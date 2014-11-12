import cPickle

proteins = cPickle.load(open('proteins.pkl'))
ids = sorted(proteins.keys())
output = open('hclust.labels', 'w')

for id in ids:
    locations = proteins[id].difference([''])
    print >> output, '\t'.join([id] + sorted(locations))
