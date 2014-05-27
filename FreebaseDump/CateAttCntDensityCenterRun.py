'''
Created on May 27, 2014
make cate att cnt
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from CateAttCntDensityCenter import *
import sys

if 3 != len(sys.argv):
    print "2 para: in cate per obj cnt + out"
    sys.exit()
    
Center = CateAttCntDensityCenterC()
Center.MakeFromCnt(sys.argv[1])
Center.dump(sys.argv[2])
print "done"