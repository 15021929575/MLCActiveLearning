import Bio.Entrez
Bio.Entrez.email = 'ringwalt@cmu.edu'
import cPickle
proteins = cPickle.load(open('proteins.pkl'))

eg = proteins.keys()
results = Bio.Entrez.read(Bio.Entrez.elink(db_from='gene', id=eg, linkname='gene_protein'))
protein_ids = [r['LinkSetDb'][0]['Link'][-1]['Id']
                 if len(r['LinkSetDb'])
                 else "NA"
               for r in results]
entrez = iter(eg)
cur_file = None
for line in Bio.Entrez.efetch(db='protein', id=protein_ids, rettype='fasta').readlines():
    if line[0] == '>':
        cur_file = open('proteins/' + entrez.next(), 'w')
    elif line[0] == '\n' and cur_file is not None:
        cur_file.close()
        cur_file = None
    if cur_file:
        cur_file.write(line)
