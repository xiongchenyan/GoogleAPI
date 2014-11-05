'''
Created on Nov 5, 2014 3:17:43 PM
@author: cx

what I do:
merge obj's cnt
what's my input:
the dir
what's my output:
One single file about obj cnt
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from cxBase.WalkDirectory import WalkDir
import sys

if 3 != len(sys.argv):
    print "Facc mid obj cnt dir + outname"
    sys.exit()
    
hObj = {}

for fname in WalkDir(sys.argv[1]):
    for line in open(fname):
        cnt,objid = line.strip().split()
        cnt = int(cnt)
        if not objid in hObj:
            hObj[objid] = cnt
        else:
            hObj[objid] += cnt
    print '%s finished' %(fname)
    
l = hObj.items()
l.sort(key=lambda item:item[1],reverse = True)

out = open(sys.argv[2],'w')
for objid,cnt in l:
    print >>out, '%s\t%d' %(objid,cnt)
out.close()
