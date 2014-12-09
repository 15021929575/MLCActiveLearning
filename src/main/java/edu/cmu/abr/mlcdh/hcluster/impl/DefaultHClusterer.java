package edu.cmu.abr.mlcdh.hcluster.impl;

import weka.core.Instances;
import edu.cmu.abr.mlcdh.hcluster.HClusterer;

@SuppressWarnings("serial")
public class DefaultHClusterer implements HClusterer {
	protected String treeFilePath;

	public DefaultHClusterer(String treeFilePath) {
		this.treeFilePath = treeFilePath;
	}

	@Override
	public String cluster(Instances instances) {
		return this.treeFilePath;
	}
}
