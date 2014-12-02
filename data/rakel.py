import hclust
import os
proteins = sorted(os.listdir('proteins'))
print len(proteins), hclust.orig_distmat.shape
assert len(proteins) == len(hclust.orig_distmat)
import sys

subset = [l.strip() for l in open(sys.argv[1])]
inds = [proteins.index(p) for p in subset]
distmat = hclust.orig_distmat[inds, inds]
clust = hclust.get_clustering(distmat)

output = open(sys.argv[2], 'w')
for line in clust:
    print >> output, line
