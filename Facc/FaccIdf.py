'''
Created on May 20, 2014
input: list of mid + facc dir
output: mid\tidf prob
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from Facc.FaccReader import FaccReaderC
from Facc.FaccBase import *
from IndriRelate.CtfLoader import *
from cxBase.base import cxBaseC,cxConf

class FaccIdfC(cxBaseC):
    def Init(self):
        self.FaccDir = ""
        self.InTargetObj = ""
        self.hTargetObj = {}
        self.CtfCenter = TermCtfC()
        self.OutName = ""
    @staticmethod
    def ShowConf():
        print "faccdir\nin\nout"
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.FaccDir = conf.GetConf('faccdir')
        self.InTargetObj = conf.GetConf('in')
        self.OutName = conf.GetConf('out')
        
        
    def LoadTargetObj(self):
        for line in open(self.InTargetObj):
            self.hTargetObj[line.strip()] = True
            
        return True
    
    def ReadFaccDf(self):
        Reader = FaccReaderC()
        Reader.opendir(self.FaccDir)
        for lFacc in Reader:
            lInFacc = []
            for Facc in lFacc:
                ObjId  = Facc.ObjId
                if ObjId in self.hTargetObj:
                    if not ObjId in lInFacc:
                        lInFacc.append(ObjId)
#                         print "get obj [%s]" %(ObjId)
            
            for ObjId in lInFacc:
                self.CtfCenter.insert(ObjId)
                
        Reader.close()
        return True
    
    def Process(self):
        self.LoadTargetObj()
        self.ReadFaccDf()
        self.CtfCenter.dump(self.OutName)
        return True
                
