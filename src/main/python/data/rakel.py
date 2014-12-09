#! /usr/bin/env python

import hclust
import os
import cPickle
#proteins = cPickle.load(open('proteins.pkl'))
#all_proteins = sorted(os.listdir('proteins'))
#proteins = [p for p in all_proteins if len(proteins[p].difference(['']))]
#print len(proteins), hclust.orig_distmat.shape
#assert len(proteins) == len(hclust.orig_distmat)
import sys

subset = [int(l.strip()) for l in open(sys.argv[1])]
#inds = [proteins.index(p) for p in subset]
distmat = hclust.orig_distmat[subset][:, subset]
clust = hclust.get_clustering(distmat)

output = open(sys.argv[2], 'w')
for line in clust:
    print >> output, line
print >> output, "-1"
