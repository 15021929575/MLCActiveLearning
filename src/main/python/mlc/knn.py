import numpy as np
import cPickle
import scipy.spatial.distance as ssd
import os

def read_labels():
    prots = cPickle.load(open('../data/proteins.pkl'))
    keys = sorted(os.listdir('../data/proteins'))
    labels = list(reduce(frozenset.union, prots.values()).difference(['']))
    labelmat = np.zeros((len(keys), len(labels)), bool)
    for i, key in enumerate(keys):
        labelmat[i] = [l in prots[key] for l in labels]
    return labelmat

def knn(distmat, labels, k=3):
    """ For n=1 to len(distmat), query n proteins.
        For each protein, get the k nearest labeled proteins and take the
        majority vote for each label.
        Return predictions with number of queried proteins on the 1st axis,
        protein on the 2nd axis, and label on the 3rd axis. """
    if type(distmat) is str:
        distmat = cPickle.load(open(distmat))
    if len(distmat.shape) == 1:
        distmat = ssd.squareform(distmat)
    predictions = np.zeros((len(distmat), len(distmat), labels.shape[1]), bool)
    queried = np.zeros(len(distmat), bool)
    for n in xrange(len(distmat)):
        unlabeled, = np.where(~ queried)
        query = np.random.choice(unlabeled)
        queried[query] = True
        for i in xrange(len(distmat)):
            closestQueries = queried[np.argsort(distmat[i, queried])[:k]]
            predictions[n, i] = np.median(labels[closestQueries], axis=0)
    return predictions

if __name__ == "__main__":
    DISTMAT = "../data/distmats/distmat-10mer-seuclidean.pkl"
    labels = read_labels()
    preds = knn(DISTMAT, labels, k=5)
    hamming = (preds ^ labels[None, :, :]).sum(axis=-1).sum(axis=-1) / float(
                  preds.shape[1] * preds.shape[2])
    print hamming
