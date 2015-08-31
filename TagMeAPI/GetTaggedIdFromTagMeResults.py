'''
Created on Aug 31, 2015 3:00:13 PM
@author: cx

what I do:
    i write the taggged wiki id from a data
what's my input:
    tag me result
what's my output:
    tagged wiki id
'''

import sys

if len(sys.argv) != 3:
    print 'I get tag me id from tagged data'
    print 'tagme result + out name'
    sys.exit()
    
    
out = open(sys.argv[2],'w')

for line in open(sys.argv[1]):
    line = line.strip()
    vCol = line.split('#')[-1].split('\t')
    
    for i in range(len(vCol)):
        if 0 == (i % 6):
            print >>out, vCol[i]
            
out.close()
print 'finished'
