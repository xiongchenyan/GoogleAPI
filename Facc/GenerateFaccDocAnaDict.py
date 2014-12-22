'''
Created on Dec 22, 2014 3:52:02 PM
@author: cx

what I do:
I generate FaccAnnotation of
DocNo->lAna[objid,name,score] as the 
what's my input:

what's my output:


'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

import pickle

from Facc.FaccDataCenter import *

import sys


if 3 != len(sys.argv):
    print "facc dir + output name"
    sys.exit()
    
Center = FaccDataCenterC()
Center.FaccDir = sys.argv[1]

hDocAna = {}

lFName = WalkDir(sys.argv[1])
for fname in lFName:
    lFaccDoc = FaccForDocC().ReadFaccDocs(fname)
    for FaccDoc in lFaccDoc:
        DocNo = FaccDoc.DocNo
        if DocNo in hDocAna:
            continue
        lAna = []
        for FaccAna in FaccDoc.lFacc:
            ObjId = FaccAna.ObjId
            score = FaccAna.Prob
            name = FaccAna.entity
            lAna.append([ObjId,name,score])
        hDocAna[DocNo] = lAna
        
        
pickle.dump(hDocAna,open(sys.argv[2],'wb'))

print "done"
        
        
            
