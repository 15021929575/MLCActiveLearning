package edu.cmu.abr.mlcdh.hcluster;

import java.io.IOException;
import java.io.Serializable;

import weka.core.Instances;

public interface HClusterer extends Serializable {
	String cluster(Instances instances) throws IOException,
	InterruptedException;
}
