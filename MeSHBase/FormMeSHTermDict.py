'''
Created on Dec 17, 2014 5:25:02 PM
@author: cx

what I do:
from term to UI dict maker
what's my input:
mesh raw data
what's my output:
dict out

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
import sys

from cxBase.Conf import cxConfC
from MeSHBase.MeSHTermCenter import MeSHTermCenterC

if 2 != len(sys.argv):
    MeSHTermCenterC.ShowConf()
    print "in"
    sys.exit()
    
    
conf = cxConfC(sys.argv[1])
InName = conf.GetConf('in')
TermCenter = MeSHTermCenterC(sys.argv[1])
TermCenter.FormDictFromRawMeSH(InName)
print "done"


