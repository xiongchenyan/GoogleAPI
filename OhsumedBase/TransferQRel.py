'''
Created on Dec 16, 2014 8:05:01 PM
@author: cx

what I do:
transfer qrel format
what's my input:

what's my output:


'''

import sys

if len(sys.argv) != 3:
    print "qrel in + out"
    sys.exit()

hRelMap={}
hRelMap['d'] = 2
hRelMap['p'] = 1
hRelMap['n'] = 0

out = open(sys.argv[2],'w')
for line in open(sys.argv[1]):
    vCol = line.strip().split('\t')
    if vCol[3] == "":
        if vCol[5] in hRelMap:
            vCol[3] = vCol[5]
        else:
            print line
            continue
    print >>out, '%s 0 %s %s' %(vCol[0],vCol[1],hRelMap[vCol[3]])
out.close()
    
