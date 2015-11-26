'''
Created on Nov 26, 2015 3:06:02 PM
@author: cx

what I do:

what's my input:

what's my output:


'''

import site

site.addsitedir("/bos/usr0/cx/PyCode/cxPyLib")
site.addsitedir("/bos/usr0/cx/PyCode/GoogleAPI")

import subprocess,os
import sys
from cxBase.WalkDirectory import WalkDir
import ntpath


if 3 != len(sys.argv):
    print 'I submit wiki id fetch job'
    print 'dump split dir + outdir' 
    sys.exit()
    
    
lFName = WalkDir(sys.argv[1])    
lCmd = ['qsub','python','FetchAllWikiIdObjIdAlignment.py']
for fname in lFName:
    OutName = sys.argv[2] + '/' + ntpath.basename(fname)
    print subprocess.check_output(lCmd + [fname,OutName])
    

    
    


    