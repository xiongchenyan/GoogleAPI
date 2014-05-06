'''
Created on May 6, 2014

@author: cx
'''


import sys

if len(sys.argv) != 3:
    print "in + out"
    sys.exit()
    
out = open(sys.argv[2],'w')

cnt = 0
OutStr = ""
for line in open(sys.argv[1]):
    cnt += 1
    if cnt == 1:
        continue
    if 0 == (cnt % 2):
        OutStr = line.strip()
    if 1 == (cnt % 2):
        OutStr += "\t" + line.strip()
        print >>out, OutStr
        
out.close() 
        