import os
import numpy as np
from scipy.spatial import distance
from Bio import pairwise2
from Bio.SubsMat import MatrixInfo as matlist
import multiprocessing
def get_score(pair):
    return pairwise2.align.localds(
              pair[0], pair[1], matlist.blosum62, -10, -0.5)[0][2]

if __name__ == "__main__":
    pool = multiprocessing.Pool(6)

    idents = sorted(os.listdir('proteins'))
    seqs = dict()
    for ident in idents:
        f = open('proteins/' + ident)
        f.readline()
        seqs[ident] = ''.join(s.strip() for s in f.readlines())
    print 'Calculating distance matrix...'
    pairs = [(seqs[idents[i]],seqs[idents[j]])
             for i in xrange(len(idents) - 1)
             for j in xrange(i+1, len(idents))]
    scores = map(get_score, pairs)
    scores = np.array(scores)
    import cPickle
    cPickle.dump(scores, open('distmats/distmat-localalign-blosum62-10-0.5.pkl', 'wb'))
