package edu.cmu.abr.mlcdh.hcluster.impl;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Paths;

import weka.core.Instance;
import weka.core.Instances;
import edu.cmu.abr.mlcdh.hcluster.HClusterer;

@SuppressWarnings("serial")
public class LabelsIncludedHClusterer implements HClusterer {
	private final String labelIncludedHClustererPath;
	private final String outputPath;
	private final String distanceMatrixFilePath;

	private final String partialLabelsFilePath;
	private final String treeFilePath;

	public LabelsIncludedHClusterer(String labelIncludedHClustererPath,
			String distanceMatrixFilePath, String outputPath) {
		this.labelIncludedHClustererPath = labelIncludedHClustererPath;
		this.distanceMatrixFilePath = distanceMatrixFilePath;
		this.outputPath = outputPath;
		this.partialLabelsFilePath = Paths.get(this.outputPath,
				"partial_labels").toString();
		this.treeFilePath = Paths.get(this.outputPath, "tree").toString();
	}

	@Override
	public String cluster(Instances instances) throws IOException,
			InterruptedException {
		this.savePartialLabelsToFile(instances);
		this.run();
		return this.treeFilePath;
	}

	private void run() throws IOException, InterruptedException {
		final String[] tokens = new String[] {
				this.labelIncludedHClustererPath, this.distanceMatrixFilePath,
				this.partialLabelsFilePath, this.treeFilePath };
		final Process process = Runtime.getRuntime().exec(tokens);
		process.waitFor();
		for (final String t : tokens) {
			System.out.print(t);
			System.out.print(" ");
		}
		System.out.println();
		assert (process.exitValue() == 0);
	}

	private void savePartialLabelsToFile(Instances instances)
			throws IOException {
		try (BufferedWriter writer = new BufferedWriter(new FileWriter(
				this.partialLabelsFilePath))) {
			for (int i = 0; i < instances.numInstances(); i++) {
				final Instance instance = instances.get(i);
				int numCommas = instances.numAttributes() - 3;
				numCommas = numCommas > 0 ? numCommas : 0;
				for (int j = 0; j < instances.numAttributes() - 1; j++) {
					if (j != instances.classIndex()) {
						writer.write(new Integer((int) instance.value(j))
								.toString());
						if (numCommas > 0) {
							writer.write(",");
							numCommas--;
						}
					}
				}
				writer.write("\n");
			}
		}
	}

}
