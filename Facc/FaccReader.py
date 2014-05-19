'''
Created on Apr 22, 2014
read facc from dir
input: facc dir
do: each time a lFaccAnnotationC
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from Facc.FaccBase import *
from cxBase.KeyFileReader import KeyFileReaderC
from cxBase.WalkDirectory import WalkDir

from cxBase.base import cxBaseC

class FaccReaderC(cxBaseC):
    #call KeyFileReader for each FaccDoc
    def Init(self):
        self.lFaccName = []
        self.Index = 0
        self.CurrentFaccReader = KeyFileReaderC()
    
    
    def SetConf(self,ConfIn):
        return
        
    def opendir(self,FaccDir):
        self.lFaccName = WalkDir(FaccDir)
        self.Index = 0
    
    def open(self,InName):
        self.lFaccName = [InName]
        self.Index = 0
        
    def close(self):
        self.CurrentFaccReader.close()
        self.Index = 0
        self.lFaccName = []
        
        
    def MoveToNextFile(self):
        if self.Index >= len(self.lFaccName):
            return False
        self.CurrentFaccReader.close()
        print "opening facc file [%d][%s]" %(self.Index,self.lFaccName[self.Index])
        self.CurrentFaccReader.open(self.lFaccName[self.Index])
        self.Index += 1
        return True
        
    def ReadNextFacc(self):
        if self.CurrentFaccReader.empty():
            if not self.MoveToNextFile():
                return []
            
        lvCol = self.CurrentFaccReader.ReadNextKey()
        if [] == lvCol:
            if not self.MoveToNextFile():
                return []
            lvCol = self.CurrentFaccReader.ReadNextKey()
            
        if [] == lvCol:
            return []
        
        #now things is in lvCol
        lFacc = []
        for line in ['\t'.join(vCol) for vCol in lvCol]:
            FaccAna = FaccAnnotationC(line)
            lFacc.append(FaccAna)
            
        return lFacc
    
    def __iter__(self):
        return self
    
    def next(self):
        lFacc = self.ReadNextFacc()
        if [] == lFacc:
            raise StopIteration
        return lFacc
            

