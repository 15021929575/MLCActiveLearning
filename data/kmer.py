import os
import pandas
import numpy as np
from scipy.spatial import distance

METRICS = ['seuclidean']

for KMERSIZE in range(10, 10):
    idents = sorted(os.listdir('proteins'))
    kmerset = set()
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
        kmer_normalized = col_kmercount.astype(float) / col_kmercount.sum()
        kmercount[ident].iloc[:len(col_kmercount)] = kmer_normalized

    kmercount = np.array(kmercount, np.float64)
    kmercount = kmercount[(kmercount != 0).sum(axis=1) > 1]
    print 'Calculating distance matrix...'
    for METRIC in METRICS:
        if METRIC == 'mahalanobis':
            S = np.cov(kmercount)
            #km = kmercount - kmercount.mean(axis=1)[:,None]
            #S = np.zeros((km.shape[0], km.shape[0]))
            #for i in xrange(len(S)):
            #    S[i,:] = (km[i,None] * km).mean(axis=1)
            S1 = np.linalg.pinv(S) # pseudo-inverse
        import scipy.spatial.distance
        distmat = scipy.spatial.distance.pdist(kmercount.T, METRIC,
                                               VI=S1 if METRIC=='mahalanobis' else None)
        import cPickle
        cPickle.dump(distmat, open('distmats/distmat-%dmer-%s.pkl' % (KMERSIZE, METRIC), 'wb'))
