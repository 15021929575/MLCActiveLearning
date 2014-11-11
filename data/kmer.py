import os
import pandas
import numpy as np
from scipy.spatial import distance

kmerset = set()

idents = sorted(os.listdir('proteins'))
kmerlists = dict()
for ident in idents:
    f = open('proteins/' + ident)
    f.readline()
    pseq = ''.join(s.strip() for s in f.readlines())
    kmerlist = [pseq[i:i+3] for i in xrange(len(pseq) - 2)]
    kmerlists[ident] = kmerlist
    kmerset.update(kmerlist)

kmerset = list(kmerset)
kmercount = pandas.DataFrame(columns=idents, index=kmerset)
kmercount.fillna(0, inplace=True)

for ident in idents:
    kmer_inds = [kmerset.index(kmer) for kmer in kmerlists[ident]]
    col_kmercount = np.bincount(kmer_inds)
    kmercount[ident].iloc[:len(col_kmercount)] = col_kmercount

kmercount = np.array(kmercount, np.float32)
import scipy.sparse
kmercount = scipy.sparse.csc_matrix(kmercount)
print 'Calculating distance matrix...'
km = kmercount - kmercount.mean(1)
norm = kmercount.shape[1] - 1
S = np.dot(km, km.T) / norm
S1 = np.linalg.inv(S).astype(np.float32)
distmat = km.T.dot(S1).dot(km) # Mahalanobis distance
import cPickle
cPickle.dump(distmat, open('distmat.pkl', 'wb'))
