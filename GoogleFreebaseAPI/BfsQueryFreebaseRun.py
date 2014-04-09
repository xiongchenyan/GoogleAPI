'''
Created on Apr 8, 2014
run bfs query freebase
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib/')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI/')

from BfsQueryFreebase import *

import sys

if 2 != len(sys.argv):
    print "1 para: conf\nin"
    BfsQueryFreebaseC().ShowConf()
    sys.exit()
    
    
BfsQueryFreebaseUnitRun(sys.argv[1])

print "finished"
