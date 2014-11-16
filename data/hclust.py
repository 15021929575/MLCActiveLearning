import cPickle
import numpy as np
import scipy.spatial.distance

KMERSIZE=3

distmat = cPickle.load(open('distmat-%dmer.pkl' % KMERSIZE))
if len(distmat.shape) == 1:
    distmat = scipy.spatial.distance.squareform(distmat)
distmat[range(len(distmat)), range(len(distmat))] = np.inf

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

tree = open('hclust-%dmer.tree' % KMERSIZE, 'w')
# Every node but the root (node len(clusters)-1) has a parent
for clust in xrange(len(clusters)-1):
    print >> tree, children.index(clust) / 2
print >> tree, -1
