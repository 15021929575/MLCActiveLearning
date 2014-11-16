import os
import pandas
import numpy as np
from scipy.spatial import distance

KMERSIZE = 3

kmerset = set()

idents = sorted(os.listdir('proteins'))
kmerlists = dict()
for ident in idents:
    f = open('proteins/' + ident)
    f.readline()
    pseq = ''.join(s.strip() for s in f.readlines())
    kmerlist = [pseq[i:i+KMERSIZE] for i in xrange(len(pseq) - (KMERSIZE-1))]
    kmerlists[ident] = kmerlist
    kmerset.update(kmerlist)

kmerset = list(kmerset)
kmercount = pandas.DataFrame(columns=idents, index=kmerset)
kmercount.fillna(0, inplace=True)

for ident in idents:
    kmer_inds = [kmerset.index(kmer) for kmer in kmerlists[ident]]
    col_kmercount = np.bincount(kmer_inds)
    kmercount[ident].iloc[:len(col_kmercount)] = col_kmercount

kmercount = np.array(kmercount, np.float64)
kmercount = kmercount[kmercount.sum(1) > 1]
print 'Calculating distance matrix...'
#km = kmercount - kmercount.mean(1)[:, None]
#norm = kmercount.shape[1] - 1
#S = np.dot(km, km.T) / norm # Covariance matrix
S = np.cov(kmercount)
#S += np.eye(len(S)) * 1e-10 # Fudge diagonal of S
#S1 = np.linalg.inv(S)
S1 = np.linalg.pinv(S) # pseudo-inverse
#kmS1 = km.T.dot(S1)
#distmat = np.sqrt(kmS1.dot(km)) # Mahalanobis distance
import scipy.spatial.distance
distmat = scipy.spatial.distance.pdist(kmercount.T, 'mahalanobis', VI=S1)
import cPickle
cPickle.dump(distmat, open('distmat-%dmer.pkl' % KMERSIZE, 'wb'))
