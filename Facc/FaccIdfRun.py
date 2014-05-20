'''
Created on May 20, 2014

@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from Facc.FaccIdf import *

import sys

if 2 != len(sys.argv):
    print "conf"
    FaccIdfC().ShowConf()
    sys.exit()
    
    
Idfer = FaccIdfC(sys.argv[1])

Idfer.Process()
print"finished"