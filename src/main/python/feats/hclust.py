#! /usr/bin/env python

import cPickle
import numpy as np
import scipy.spatial.distance as ssd
import os
import re

def load_distmat(distmat_file_path):
    proteins = cPickle.load(open('../../resources/proteins.pkl'))
    all_proteins = sorted(os.listdir('proteins'))
    protein_labeled_mask = np.array([len(proteins[p].difference([''])) != 0
                            for p in all_proteins])
    distmat = cPickle.load(open(distmat_file_path))
    if len(distmat.shape) == 1:
        distmat = ssd.squareform(distmat)
    distmat = distmat[protein_labeled_mask][:, protein_labeled_mask]
    distmat[range(len(distmat)), range(len(distmat))] = np.inf
    return distmat

def new_distmat(distmat, features):
    newfeat_dist = ssd.squareform(ssd.pdist(features, 'seuclidean'))
    # This is equivalent to adding new features when calculating the
    # original distance, assuming Euclidean distance
    new_dists = np.sqrt(distmat**2 + newfeat_dist**2)
    new_dists[range(len(new_dists)), range(len(new_dists))] = np.inf
    return new_dists

def get_clustering(distmat):
    clusters = [[i] for i in xrange(len(distmat))]
    centroids = range(len(distmat))
    cur_clusters = range(len(distmat))
    children = [None for i in xrange(len(distmat)) for j in range(2)]

    while len(cur_clusters) > 1:
        cur_centroids = [centroids[i] for i in cur_clusters]
        centroids_dist = distmat[cur_centroids][:,cur_centroids]
        join_x, join_y = np.unravel_index(centroids_dist.argmin(), centroids_dist.shape)
        clust_x = cur_clusters[join_x]
        clust_y = cur_clusters[join_y]
        newclust = clusters[clust_x] + clusters[clust_y]
        newclust_dists = distmat[newclust][:, newclust]
        newclust_centroid = newclust_dists.max(axis=1).argmin()
        clusters.append(newclust)
        centroids.append(newclust[newclust_centroid])
        cur_clusters.remove(clust_x)
        cur_clusters.remove(clust_y)
        cur_clusters.append(len(clusters) - 1)
        children += [clust_x, clust_y]
    # Every node but the root (node len(clusters)-1) has a parent
    return [children.index(clust) / 2 for clust in xrange(len(clusters)-1)]

def main(args):
    distmat = load_distmat(args[1])
    clustering = get_clustering(distmat)
    tree = open(args[2], 'w')
    for parent in clustering:
        print >> tree, parent
    print >> tree, -1

if __name__ == '__main__':
    import sys
    main(sys.argv)
