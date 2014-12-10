package edu.cmu.abr.mlcdh.hcluster.impl;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Paths;

import weka.core.Instance;
import weka.core.Instances;
import edu.cmu.abr.mlcdh.hcluster.HClusterer;

@SuppressWarnings("serial")
public class SubsetHClusterer implements HClusterer {
	private final String subsetHClustererPath;
	private final String outputPath;

	private final String subsetFilePath;
	private final String treeFilePath;

	public SubsetHClusterer(String subsetHClustererPath, String outputPath) {
		this.subsetHClustererPath = subsetHClustererPath;
		this.outputPath = outputPath;
		this.subsetFilePath = Paths.get(this.outputPath, "subset").toString();
		this.treeFilePath = Paths.get(this.outputPath, "tree").toString();
	}

	@Override
	public String cluster(Instances instances) throws IOException,
			InterruptedException {
		this.saveSubsetToFile(instances);
		this.run();
		return this.treeFilePath;
	}

	private void run() throws IOException, InterruptedException {
		final Process process = Runtime.getRuntime().exec(
				new String[] { this.subsetHClustererPath, this.subsetFilePath,
						this.treeFilePath }, null,
				new File(this.subsetHClustererPath).getParentFile());
		process.waitFor();
		if (process.exitValue() != 0) {
			throw new IOException("HClusterer failed");
		}
	}

	private void saveSubsetToFile(Instances instances) throws IOException {
		try (BufferedWriter writer = new BufferedWriter(new FileWriter(
				this.subsetFilePath))) {
			for (int i = 0; i < instances.numInstances(); i++) {
				final Instance instance = instances.get(i);
				assert (instance.attribute(instances.numAttributes() - 1)
						.name().equals("index"));
				writer.write(new Integer((int) instance.value(instance
						.numAttributes() - 1)).toString() + "\n");
			}
		}
	}
}
