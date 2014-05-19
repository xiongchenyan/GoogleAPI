'''
Created on May 19, 2014

@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from Facc.MakeFaccDocForQuery import FaccDocMakerC
import sys


if 2 != len(sys.argv):
    print "conf:"
    FaccDocMakerC.ShowConf()
    sys.exit()

FaccDocMakerC.Process()
print "finished"    
