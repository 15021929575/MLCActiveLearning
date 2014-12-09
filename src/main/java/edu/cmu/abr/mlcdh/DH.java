package edu.cmu.abr.mlcdh;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import weka.classifiers.Classifier;
import weka.classifiers.RandomizableClassifier;
import weka.core.Attribute;
import weka.core.Capabilities;
import weka.core.Capabilities.Capability;
import weka.core.Instance;
import weka.core.Instances;
import edu.cmu.abr.mlcdh.hcluster.HClusterer;

@SuppressWarnings("serial")
public class DH extends RandomizableClassifier implements Classifier {
	private final HClusterer hClusterer;
	private final String outputPath;
	private final String dhPath;
	private final int selectType;
	private final int period;
	private int numLabels;
	private static int currentWindow;
	private final Map<Integer, List<Integer>> predictions;
	private final Instances instancesTemplate;

	public static final int DEFAULT_SELECT_TYPE = 1;
	public static final int DEFAULT_PERIOD = 1;

	public static String dhOutputFilenamePrefix = "predictions_at_iteration";
	public static String labelsFilename = "labels";

	public DH(HClusterer hClusterer, String outputPath, String dhPath,
			int selectType, int period, int numLabels) {
		super();
		this.hClusterer = hClusterer;
		this.outputPath = outputPath;
		this.dhPath = dhPath;
		this.numLabels = numLabels;
		this.selectType = selectType;
		this.period = period;
		this.predictions = new HashMap<Integer, List<Integer>>();
		final ArrayList<Attribute> attributes = new ArrayList<Attribute>();
		attributes.add(new Attribute("label"));
		attributes.add(new Attribute("index"));
		this.instancesTemplate = new Instances("Instances template",
				attributes, 0);
		this.instancesTemplate.setClassIndex(0);
	}

	public DH(HClusterer hClusterer, String outputPath, String dhPath,
			int numLabels) {
		this(hClusterer, outputPath, dhPath, DEFAULT_SELECT_TYPE,
				DEFAULT_PERIOD, numLabels);
	}

	@Override
	public void buildClassifier(Instances instances) throws Exception {
		this.numLabels = Utils.saveInstancesToSingleLabelFile(instances, Paths
				.get(this.outputPath, labelsFilename).toString());
		this.run(this.hClusterer.cluster(instances));
		this.loadAllDhFiles(instances.numInstances());
		DH.setCurrentWindow(1);
	}

	@Override
	public double classifyInstance(Instance instance) throws Exception {
		List<Integer> currentPrediction = this.predictions
				.get(DH.currentWindow);
		if (currentPrediction == null) {
			currentPrediction = Utils.loadSingleLabelFileToList(Paths.get(
					this.outputPath,
					dhOutputFilenamePrefix + "." + currentWindow).toString());
			this.predictions.put(currentWindow, currentPrediction);
		}
		return currentPrediction.get((int) instance.value(1));
	}

	@Override
	public double[] distributionForInstance(Instance instance) throws Exception {
		final double label = this.classifyInstance(instance);
		final double[] distribution = new double[this.numLabels];
		distribution[(int) label] = 1.0;
		return distribution;
	}

	@Override
	public Capabilities getCapabilities() {
		final Capabilities capabilities = super.getCapabilities();
		capabilities.enable(Capability.NOMINAL_ATTRIBUTES);
		capabilities.enable(Capability.NUMERIC_ATTRIBUTES);
		capabilities.enable(Capability.NOMINAL_CLASS);
		return capabilities;
	}

	private void run(String treeFilePath) throws IOException,
	InterruptedException {
		final String[] tokens = new String[] { this.dhPath, "--seed",
				new Integer(this.getSeed()).toString(), "--sel_type",
				new Integer(this.selectType).toString(), "--period",
				new Integer(this.period).toString(),
				new Integer(this.numLabels).toString(), treeFilePath,
				Paths.get(this.outputPath, labelsFilename).toString(),
				Paths.get(this.outputPath, dhOutputFilenamePrefix).toString() };
		final Process process = Runtime.getRuntime().exec(tokens);
		for (final String t : tokens) {
			System.out.print(t);
			System.out.print(" ");
		}
		System.out.println();
		process.waitFor();
		assert (process.exitValue() == 0);
	}

	public static int getCurrentWindow() {
		return DH.currentWindow;
	}

	public static void setCurrentWindow(int currentWindow) {
		DH.currentWindow = currentWindow;
	}

	private void loadAllDhFiles(int numInstances) throws IOException {
		for (int window = 1; window < numInstances; window += this.period) {
			this.predictions.put(
					window,
					Utils.loadSingleLabelFileToList(Paths.get(this.outputPath,
							dhOutputFilenamePrefix + "." + window).toString()));
		}
		this.predictions
		.put(numInstances, Utils
				.loadSingleLabelFileToList(Paths.get(this.outputPath,
						dhOutputFilenamePrefix + "." + numInstances)
						.toString()));
	}
}
