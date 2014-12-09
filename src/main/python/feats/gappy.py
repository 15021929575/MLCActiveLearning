import copy
import numpy as np
import cPickle
import os
import scipy.spatial.distance as ssd
LETTERS = map(chr, range(ord('A'), ord('Z')+1))
class Instance:
    string = None
    i = None
    label = None
class Trie:
    g = None
    k = None
    instances = None
    children = None
    def __init__(self, g, k):
        self.g = g
        self.k = k
    def child(self, x):
        if self.children is None:
            self.children = [None for i in LETTERS]
        i = LETTERS.index(x)
        if self.children[i] is None:
            self.children[i] = Trie(g, k)
        return self.children[i]
    def insert(self, inst):
        if self.instances is None:
            self.instances = set()
        self.instances.add(inst)
        for l in LETTERS:
            ind = inst.string.find(l, inst.i)
            if ind >= 0:
                new_inst = copy.copy(inst)
                new_inst.i = ind+1
                self.child(l).insert(new_inst)

def kmers(seqs, labels, k):
    A = []
    L = []
    for seq, label in zip(seqs, labels):
        A.extend([seq[i:i+k] for i in xrange(len(seq)-k+1)])
        L.extend([label for i in xrange(len(seq)-k+1)])
    return A, L
def gappysubdist(prefix, gmers, inds, labels, nl, g, k):
    dists = np.zeros(nl*(nl-1)/2)
    if len(prefix) == k:
        counts = np.zeros(nl)
        counts2 = np.bincount(labels)
        counts[:len(counts2)] = counts2
        if not (np.std(counts) > 0.01):
            return dists
        else:
            counts = counts.astype(np.float64) / np.std(counts)
            i = 0
            for a in xrange(nl-1):
                dists[i:i+nl-a-1] += (counts[a] - counts[a+1:]) ** 2
                i += nl-a-1
            return dists
    else:
        allfeats = []
        for l in LETTERS:
            new_inds = [g.find(l, ind) for g, ind in zip(gmers, inds)]
            new_gmers = [g for g,ind in zip(gmers, new_inds) if ind >= 0]
            new_labels = [lab for lab,ind in zip(labels, new_inds) if ind >= 0]
            new_inds = [ind+1 for ind in new_inds if ind >= 0]
            dists += gappysubdist(prefix + l, new_gmers,
                                          new_inds, new_labels,
                                          nl, g, k)
        return dists
def gappydist(seqs, labels, g, k):
    nl = max(labels) + 1
    gmers, labels = kmers(seqs, labels, g)
    return np.sqrt(gappysubdist('', gmers, [0 for gmer in gmers],
                                labels, nl, g, k))

G = 8
K = 4
if __name__ == '__main__':
    seqs = []
    idents = sorted(os.listdir('proteins'))
    for ident in idents:
        f = open('proteins/' + ident)
        f.readline()
        seqs.append(''.join(l.strip() for l in f))
    labels = range(len(seqs))
    distmat = gappydist(seqs, labels, G, K)
    cPickle.dump(distmat, open('distmats/distmat-%d,%d-gappy-seuclidean.pkl'
                                  % (G, K), 'wb'))
