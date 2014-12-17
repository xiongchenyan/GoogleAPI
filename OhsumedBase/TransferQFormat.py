'''
Created on Dec 16, 2014 5:54:41 PM
@author: cx

what I do:
transfer query to web track query format
what's my input:
ohsumed query
what's my output:
with web track format

'''

import sys
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.TextBase import TextBaseC

if 3 != len(sys.argv):
    print "ohsumed query + output"
    sys.exit()
    
out = open(sys.argv[2],'w')

LastLine = ""
qid = ""
query = ""
for line in open(sys.argv[1]):
    line = line.strip()
    if line[:2] == ".I":
        qid = line.split()[1]
    if LastLine == ".W":
        query = TextBaseC.RawClean(line)
        print >>out, qid + '\t' + query
    LastLine = line

out.close()
print "finished"
        
