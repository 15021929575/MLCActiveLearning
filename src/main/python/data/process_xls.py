import requests
import time
import xlrd
book = xlrd.open_workbook('JCB_201303145_TableS1.xls')
sheet = book.sheet_by_index(0)
proteins_orig = dict((row[0].strip(),
                 frozenset([' '.join(field.split()[1:])
                            for field in row[3:20]]))
                for rownum in xrange(1, 178)
                for row in [sheet.row_values(rownum)])
proteins = dict()

for horf, v in proteins_orig.iteritems():
    horf_id, position = horf.split('@')
    sess = requests.Session()
    sess.headers.update({'referer': 'http://horfdb.dfci.harvard.edu/hv5/index.php?page=getresults&by=plate&qury=' + horf_id})
    result = sess.post('http://horfdb.dfci.harvard.edu/hv5/convert.php',
                    data=dict(by='plate', limit='', qlist=horf_id))
    lines = result.iter_lines()
    lines.next() # initial blank line
    header = lines.next().strip().split('\t')
    position_col = header.index('Resource_Position')
    entrez_col = header.index('ENTREZ_GENE_ID')
    for line in lines:
        line = line.strip().split('\t')
        if line[position_col] == position:
            proteins[line[entrez_col]] = v
            break
    else:
        import pdb
        pdb.set_trace()

import cPickle
cPickle.dump(proteins, open('proteins.pkl', 'wb'))
