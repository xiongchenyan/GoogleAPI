'''
Created on May 19, 2014

@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from Facc.FaccReader import FaccReaderC
from Facc.FaccBase import *

        
        
class FaccForDocC(object):
    def Init(self):
        self.lFacc = []   #contains FaccAnnotationC()
        self.DocNo = ""
        
    def __init__(self,lFacc = []):
        self.Init()
        if [] != lFacc:
            self.Set(lFacc)
            
    def Set(self,lFacc):
        self.lFacc = list(lFacc)
        self.DocNo = lFacc[0].DocNo
        
    def dumps(self):
        res = ""
        for facc in self.lFacc:
            res += facc.dumps() + "\n"
        return res.strip()
    
    
    @staticmethod
    def ReadFaccDocs(InName):
        Reader = FaccReaderC()
        Reader.open(InName)
        lFaccDoc = []
        for lFacc in Reader:
            lFaccDoc.append(FaccForDocC(lFacc))
        return lFaccDoc
    
    @staticmethod
    def DumpFaccDocs(lFaccDoc, OutName):
        out = open(OutName,'w')
        for FaccDoc in lFaccDoc:
            print >>out, FaccDoc.dumps()
        out.close()
        return True
        
    