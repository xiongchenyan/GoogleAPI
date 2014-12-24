'''
Created on Dec 24, 2014 2:52:34 PM
@author: cx

what I do:
prepare mesh term objects
what's my input:
raw mesh in
what's my output:
meshterm dict

'''


import site

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
from ObjCenter.MeSHObjCacheCenter import MeSHObjCacheCenterC
from cxBase.Conf import cxConfC

import sys

if 2 != len(sys.argv):
    MeSHObjCacheCenterC.ShowConf()
    print "in"
    sys.exit()
    
CacheCenter = MeSHObjCacheCenterC(sys.argv[1])
conf = cxConfC(sys.argv[1])
InName = conf.GetConf('in')

CacheCenter.FormMeSHTermDict(InName)
print "finished"
