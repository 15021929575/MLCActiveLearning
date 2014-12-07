import numpy as np
import os
import cPickle
proteins = cPickle.load(open('proteins.pkl'))
all_proteins = sorted(os.listdir('proteins'))
proteins = [p for p in all_proteins if len(proteins[p].difference(['']))]
import sys

import scipy.spatial.distance as ssd
old_distmat = cPickle.load(open(sys.argv[1]))
if len(old_distmat.shape) == 2:
    old_distmat = ssd.squareform(old_distmat)

feats = np.loadtxt(sys.argv[2], delimiter=',')
featdist = ssd.pdist(feats.T, 'seuclidean')
new_distmat = old_distmat + feats
cPickle.dump(new_distmat, open(sys.argv[3], 'w'))
