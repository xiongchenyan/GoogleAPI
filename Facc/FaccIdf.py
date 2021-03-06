'''
Created on May 20, 2014
input: list of mid + facc dir
output: mid\tidf prob
@author: cx
'''

'''
Feb 22
if in is not given, will count all objects in facc annotation
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from Facc.FaccReader import FaccReaderC
from Facc.FakbaReader import FakbaReaderC
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
        self.InType = 'facc'
    @staticmethod
    def ShowConf():
        print "faccdir\nin\nout\ninputtype facc|fakba"
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.FaccDir = conf.GetConf('faccdir')
        self.InTargetObj = conf.GetConf('in')
        self.OutName = conf.GetConf('out')
        self.InType = conf.GetConf('fakba')
        
        
    def LoadTargetObj(self):
        if "" == self.InTargetObj:
            return
        for line in open(self.InTargetObj):
            self.hTargetObj[line.strip()] = True
            
        return True
    
    def ReadFaccDf(self):
        if self.InType == 'facc':
            Reader = FaccReaderC()
        else:
            Reader = FakbaReaderC()
        Reader.opendir(self.FaccDir)
        for lFacc in Reader:
            lInFacc = []
            for Facc in lFacc:
                ObjId  = Facc.ObjId
                if (ObjId in self.hTargetObj) | (len(self.hTargetObj) == 0):
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
                
