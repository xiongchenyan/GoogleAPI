'''
Created on Apr 18, 2014
split the gzip dump to gzip
@author: cx
'''



import gzip
import sys

if len(sys.argv) != 4:
    print "3 para: in gzip + output dir + line per split"
    print "possible filter to be added"
    sys.exit()
    
    
cnt = 0
OutCnt = 0
MaxCnt = int(sys.argv[3])
OutDir = sys.argv[2]
f_out = gzip.open(OutDir + "/%d" %(OutCnt),'wb')

LastKey = ""
for line in gzip.open(sys.argv[1]):
    line = line.strip()
    vCol = line.split('\t')
    key = vCol[0]
    
    if LastKey == "":
        LastKey = key
    if LastKey != key:
        if cnt >= MaxCnt:
            print "split [%d] finished with [%d] line" %(OutCnt,cnt)
            cnt = 0
            OutCnt += 1
            f_out.close()
            f_out = gzip.open(OutDir + "/%d" %(OutCnt),'wb')
        LastKey = key
        
    print >>f_out,line
    
f_out.close()
        