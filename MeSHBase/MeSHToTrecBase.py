'''
Created on Dec 17, 2014 3:58:35 PM
@author: cx

what I do:
transfer MeSH data to TrecWeb format, for indri retrieval.
what's my input:
MeSh.txt
what's my output:
trec web format

'''
import sys
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from IndriRelate.TrecWebDoc import TrecWebDocC


if len(sys.argv) != 3:
    print "MeSH corpus in + out"
    sys.exit()
    
out = open(sys.argv[2],'w')

lLines = []
cnt = 0
for line in open(sys.argv[1]):
    line = line.strip()
    if '*NEWRECORD' == line:
        TrecDoc = TrecWebDocC(lLines)
        print >>out, TrecDoc.dumps()
        lLines = []
        cnt += 1
        if 0 == (cnt % 1000):
            print 'processed [%d] doc' %(cnt)
    lLines.append(line)
TrecDoc = TrecWebDocC(lLines)
print >>out, TrecDoc.dumps()    
out.close()
print "finished"