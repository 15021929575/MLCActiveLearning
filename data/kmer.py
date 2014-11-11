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
    kmerlist = [pseq[i:i+4] for i in xrange(len(pseq) - 3)]
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
print 'Calculating distance matrix...'
S = np.cov(kmercount.T)
S1 = np.linalg.inv(S).astype(np.float32)
km = kmercount - kmercount.mean(axis=1)[:,None]
kmS = km.dot(S1)
distmat = np.sqrt(kmS.dot(km.T))
#distmat = distance.pdist(kmercount, 'mahalanobis')
