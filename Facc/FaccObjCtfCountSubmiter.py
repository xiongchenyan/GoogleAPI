'''
Created on Nov 5, 2014 2:58:49 PM
@author: cx

what I do:
submit jobs to run count the obj frequency in one file
what's my input:
FACC1 dir
what's my output:
a dir of output counts: 

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from cxBase.WalkDirectory import WalkDir
import subprocess
import sys
import json

if 3 != len(sys.argv):
    print "Facc dir + outmiddir"
    sys.exit()

lCmd=['qsub','/bos/usr0/cx/tmp/FACC1/Stats/ObjFreq/Count.sh']
lFName = WalkDir(sys.argv[1])

cnt = 0
for FName in lFName:
    OutName = "%s/%d"  %(sys.argv[2],cnt)
    subprocess.check_output(lCmd + [FName,OutName])
    print json.dumps(lCmd + [FName,OutName])
    cnt += 1
    
print "all submitted"


