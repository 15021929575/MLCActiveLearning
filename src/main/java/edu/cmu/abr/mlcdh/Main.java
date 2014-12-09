package edu.cmu.abr.mlcdh;

import java.io.FileWriter;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

import meka.classifiers.multilabel.BR;
import meka.classifiers.multilabel.CC;
import meka.classifiers.multilabel.Evaluation;
import meka.classifiers.multilabel.MultilabelClassifier;
import meka.classifiers.multilabel.RAkEL;
import meka.core.Result;
import weka.classifiers.RandomizableClassifier;
import weka.core.Instances;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import edu.cmu.abr.mlcdh.hcluster.impl.DefaultHClusterer;
import edu.cmu.abr.mlcdh.hcluster.impl.LabelsIncludedHClusterer;

public class Main {
	public static void main(String[] args) throws Exception {
		for (final String arg : args) {
			System.out.println(arg);
		}

		final String reductionType = args[0];
		final String labelsFilePath = args[1];
		final int numLabels = Integer.parseInt(args[2]);
		final String outputDirPath = args[3];
		final String dhPath = args[4];

		final int period = 1;
		final MultilabelClassifier classifier = makeClassifier(reductionType,
				numLabels, outputDirPath, dhPath, args);

		final Instances instances = Utils.loadMultiLabelFileToInstances(
				numLabels, labelsFilePath);

		classifier.buildClassifier(instances);

		final Map<String, List<Double>> evaluations = new HashMap<String, List<Double>>();
		for (int window = 1; window < instances.numInstances(); window += period) {
			collectEvaluation(classifier, instances, window, evaluations);
		}
		collectEvaluation(classifier, instances, instances.numInstances(),
				evaluations);

		System.out.println(evaluations.toString());

		try (FileWriter writer = new FileWriter(Paths.get(outputDirPath,
				"evaluations.json").toString())) {
			final Gson gson = new GsonBuilder().setPrettyPrinting().create();
			gson.toJson(evaluations, writer);
		}
	}

	private static void collectEvaluation(
			final MultilabelClassifier classifier, final Instances instances,
			int window, Map<String, List<Double>> evaluations) throws Exception {
		final Map<String, Double> results = evaluate(classifier, instances,
				window);
		for (final Map.Entry<String, Double> entry : results.entrySet()) {
			final String metric = entry.getKey();
			final Double value = entry.getValue();
			List<Double> values = evaluations.get(metric);
			if (values == null) {
				values = new ArrayList<Double>();
				evaluations.put(metric, values);
			}
			values.add(value);
		}
	}

	@SuppressWarnings("serial")
	private static MultilabelClassifier makeClassifier(String reductionType,
			int numLabels, String outputDirPath, String dhPath, String[] args) {
		MultilabelClassifier classifier;
		RandomizableClassifier dh;
		final int seed = (new Random()).nextInt();
		switch (reductionType) {
		case "BR":
			// args[5] is tree file path
			dh = new DH(new DefaultHClusterer(args[5]), outputDirPath, dhPath,
					numLabels);
			classifier = new BR();
			break;
		case "RAkEL":
			// args[5] is tree file path
			dh = new DH(new DefaultHClusterer(args[5]), outputDirPath, dhPath,
					numLabels);
			classifier = new RAkEL() {
				{
					this.setK(100);
					this.setSeed(seed);
				}
			};
			break;
		case "CC":
			// args[5] is labels included hclusterer path
			// args[6] is distance matrix file path
			dh = new DH(new LabelsIncludedHClusterer(args[5], args[6],
					outputDirPath), outputDirPath, dhPath, numLabels);
			classifier = new CC() {
				{
					this.setSeed(seed);
				}
			};
			break;
		default:
			throw new Error("Unknown reduction type");
		}
		dh.setSeed(seed);
		classifier.setClassifier(dh);
		classifier.setDebug(true);
		return classifier;
	}

	private static Map<String, Double> evaluate(
			MultilabelClassifier classifier, Instances instances, int window)
			throws Exception {
		DH.setCurrentWindow(window);
		final Result result = Evaluation.testClassifier(classifier, instances);
		result.setInfo("Type", "ML");
		result.setInfo("Threshold", "0.9");
		return Result.getStats(result, "2");
	}
}
