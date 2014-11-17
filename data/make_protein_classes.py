import cPickle
import os

# Warning: this will be incorrect if files modified in proteins/ in between
# running this and kmer.py!

proteins = cPickle.load(open('proteins.pkl'))
output = open('hclusts/hclust.labels', 'w')

distmat_ids = sorted(os.listdir('proteins'))

for id in distmat_ids:
    locations = proteins[id].difference([''])
    print >> output, '\t'.join([id] + sorted(locations))
