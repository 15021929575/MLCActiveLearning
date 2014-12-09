import os
import numpy as np
from scipy.spatial import distance
from Bio import AlignIO, Alphabet
import tempfile
import subprocess
from cStringIO import StringIO
fasta = tempfile.NamedTemporaryFile()

idents = sorted(os.listdir('proteins'))
for ident in idents:
    fasta.write(open('proteins/' + ident).read())
fasta.flush()
print 'Calculating multiple alignment...'
aligner = subprocess.Popen([
    "/tmp/muscle3.8.31_i86linux64",
    "-clwstrict",
    "-in",
    fasta.name,
    "-out",
    "-"],
    stdout=subprocess.PIPE)
stdout, stderr = aligner.communicate()
align = AlignIO.read(StringIO(stdout), 'clustal',
                     alphabet=Alphabet.ProteinAlphabet())

from Bio.SubsMat import MatrixInfo

def score_match(pair, matrix):
    if pair not in matrix:
        return matrix[(tuple(reversed(pair)))]
    else:
        return matrix[pair]

def score_pairwise(seq1, seq2, matrix, gap_s, gap_e):
    score = 0
    gap = False
    for i in range(len(seq1)):
        pair = (seq1[i], seq2[i])
        if not gap:
            if '-' in pair:
                gap = True
                score += gap_s
            else:
                score += score_match(pair, matrix)
        else:
            if '-' not in pair:
                gap = False
                score += score_match(pair, matrix)
            else:
                score += gap_e
    return score

distmat = np.zeros((len(align)-1)*(len(align)-2)/2)
ind = 0
for i in xrange(len(align)-1):
    for j in xrange(i+1,len(align)):
        distmat[ind] = score_pairwise(align[i],align[j], blosum, 1, 1)
        ind += 1
import cPickle
cPickle.dump(align, open('distmats/distmat-alignment.pkl', 'wb'))
