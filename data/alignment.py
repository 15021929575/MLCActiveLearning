import os
import numpy as np
from scipy.spatial import distance
from Bio import pairwise2
from Bio.SubsMat import MatrixInfo as matlist

idents = sorted(os.listdir('proteins'))
seqs = dict()
for ident in idents:
    f = open('proteins/' + ident)
    f.readline()
    seqs[ident] = ''.join(s.strip() for s in f.readlines())
print 'Calculating distance matrix...'
distmat = np.empty(len(idents) * (len(idents)-1) / 2)
ind = 0
for i in xrange(len(idents) - 1):
    for j in xrange(i+1, len(idents)):
        aln_i, aln_j, score, begin, end = pairwise2.align.localds(
            seqs[idents[i]], seqs[idents[j]], matlist.blosum62,
            -10, -0.5)[0]
        distmat[ind] = score
        ind += 1
import cPickle
cPickle.dump(distmat, open('distmats/distmat-localalign-blosum62-10-0.5.pkl', 'wb'))
