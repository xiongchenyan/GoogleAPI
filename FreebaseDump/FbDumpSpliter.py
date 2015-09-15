'''
Created on Sep 15, 2015 5:07:55 PM
@author: cx

what I do:
    Split fb dump gz file,
    same record kept in same file
what's my input:
    fb dump
    line per gz file
what's my output:
    splitted gz file

'''

import site
site.addsitedir("/bos/usr0/cx/PyCode/cxPyLib")
from FbDumpReader import *


import sys

if 4 != len(sys.argv):
    print 'dumpfile + line per file (1000000 suggested) + out pre fix'
    sys.exit()
    
    
    

reader = FbDumpReaderC()
reader.open(sys.argv[1])
MaxLineCnt = int(sys.argv[2])

cnt = 0
out = gzip.open(sys.argv[3] + '.%d' %(cnt),'w')
ThisCnt = 0
print 'start writing [%d] part' %(cnt)
for lvCol in reader:
    print >> out,'\n'.join(['\t'.join(vCol) for vCol in lvCol])
    ThisCnt += len(lvCol)
    if ThisCnt >= MaxLineCnt:
        ThisCnt = 0
        out.close()
        cnt += 1
        out = gzip.open(sys.argv[3] + '.%d' %(cnt),'w')
        print 'start writing [%d] part' %(cnt)
        
out.close()
print 'finished'
    