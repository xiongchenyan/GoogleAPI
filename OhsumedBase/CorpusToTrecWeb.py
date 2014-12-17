'''
Created on Dec 16, 2014 7:09:39 PM
@author: cx

what I do:
transfer corpus to TrecWeb format
what's my input:
oshmued corpus
what's my output:
trecweb format data
'''

import sys
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from IndriRelate.TrecWebDoc import TrecWebDocC


if len(sys.argv) != 3:
    print "oshumed corpus in + out"
    sys.exit()
    
out = open(sys.argv[2],'w')

lLines = []
cnt = 0
for line in open(sys.argv[1]):
    line = line.strip()
    if '.I' == line[:2]:
        TrecDoc = TrecWebDocC(lLines)
        print >>out, TrecDoc.dumps()
        lLines = []
        cnt += 1
        if 0 == (cnt % 1000):
            print 'processed [%d] doc' %(cnt)
    lLines.append(line)
    
out.close()
print "finished"
