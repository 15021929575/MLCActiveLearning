#! /usr/bin/env python

import numpy as np
import os
import cPickle
import sys
import scipy.spatial.distance as ssd
import hclust

def update_distmat(old_distmat, feats):
    if len(feats) == 0:
        return old_distmat
    if len(feats.shape) == 1:
        feats = feats.reshape(len(feats), 1)
    featdist = ssd.squareform(ssd.pdist(feats, 'seuclidean'))
    return np.sqrt(old_distmat**2 + featdist**2)

if __name__ == '__main__':
    old_distmat = cPickle.load(open(sys.argv[1]))
    feats = np.loadtxt(sys.argv[2], delimiter=',')
    new_distmat = update_distmat(old_distmat, feats)
    clustering = hclust.get_clustering(new_distmat)
    tree = open(sys.argv[3], 'w')
    for parent in clustering:
        print >> tree, parent
    print >> tree, -1
