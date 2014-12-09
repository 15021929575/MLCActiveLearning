package edu.cmu.abr.mlcdh;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import weka.core.Attribute;
import weka.core.DenseInstance;
import weka.core.Instance;
import weka.core.Instances;

public class Utils {
	private static final List<String> BINARY_VALUES;

	public static final Attribute INDEX_ATTRIBUTE;

	static {
		BINARY_VALUES = new ArrayList<String>(2);
		BINARY_VALUES.add("0");
		BINARY_VALUES.add("1");
		INDEX_ATTRIBUTE = new Attribute("index");
	}

	public static int saveInstancesToSingleLabelFile(Instances instances,
			String filePath) throws IOException {
		try (BufferedWriter writer = new BufferedWriter(
				new FileWriter(filePath))) {
			int maxLabel = 0;
			for (int i = 0; i < instances.numInstances(); i++) {
				final Instance instance = instances.get(i);
				final int label = (int) instance.classValue();
				maxLabel = label > maxLabel ? label : maxLabel;
				writer.write(new Integer(label).toString() + "\n");
			}
			return maxLabel + 1;
		}
	}

	public static Instances loadSingleLabelFileToInstances(
			Instances instancesTemplate, String filePath) throws IOException {
		try (BufferedReader reader = new BufferedReader(
				new FileReader(filePath))) {
			String line;
			int index = 0;
			final Instances instances = new Instances(instancesTemplate);
			while ((line = reader.readLine()) != null) {
				final double label = Integer.parseInt(line);
				final Instance instance = new DenseInstance(1.0, new double[] {
						label, index });
				instances.add(instance);
				index++;
			}
			return instances;
		}
	}

	public static void saveInstancesToMultiLabelFile(Instances instances,
			String filePath) throws IOException {

	}

	public static Instances loadMultiLabelFileToInstances(int numLabels,
			String filePath) throws IOException {
		try (BufferedReader reader = new BufferedReader(
				new FileReader(filePath))) {
			final ArrayList<Attribute> attributes = new ArrayList<Attribute>(
					numLabels + 1);
			for (int j = 0; j < numLabels; j++) {
				attributes.add(new Attribute("label" + j, BINARY_VALUES));
			}
			attributes.add(INDEX_ATTRIBUTE);
			final Instances instances = new Instances("Multilabel instances",
					attributes, 0);
			instances.setClassIndex(numLabels);

			String line;
			int index = 0;
			while ((line = reader.readLine()) != null) {
				final double[] values = new double[numLabels + 1];
				for (final String label : line.split(",")) {
					values[Integer.parseInt(label)] = 1.0;
				}
				values[numLabels] = index;
				final Instance instance = new DenseInstance(1.0, values);
				instances.add(instance);
				index++;
			}
			return instances;
		}
	}

	public static List<Integer> loadSingleLabelFileToList(String filePath)
			throws IOException {
		try (BufferedReader reader = new BufferedReader(
				new FileReader(filePath))) {
			String line;
			final List<Integer> labels = new ArrayList<Integer>();
			while ((line = reader.readLine()) != null) {
				final String[] tokens = line.split(" ");
				final int index = Integer.parseInt(tokens[0]);
				final int label = Integer.parseInt(tokens[1]);
				while (!(index < labels.size())) {
					labels.add(null);
				}
				labels.set(index, label);
			}
			return labels;
		}
	}
}
