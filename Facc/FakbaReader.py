'''
Created on Feb 12, 2015 11:58:52 AM
@author: cx

what I do:
I read Fakba directory
what's my input:
Fakba annotation dir
what's my output:
lFaccbase for each files 

'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from Facc.FaccBase import *
from cxBase.SeparatorlineFileReader import SeparatorlineFileReaderC
from cxBase.WalkDirectory import WalkDir

from cxBase.base import cxBaseC

class FakbaReaderC(cxBaseC):
    #call KeyFileReader for each FaccDoc
    def Init(self):
        self.lFaccName = []
        self.Index = 0
        self.CurrentReader = SeparatorlineFileReaderC(SeparatorPre='trec',KeepSepLine=True)
    
    
        
    def opendir(self,FaccDir):
        self.lFaccName = WalkDir(FaccDir)
        self.Index = 0
    
    def open(self,InName):
        self.lFaccName = [InName]
        self.Index = 0
        
    def close(self):
        self.CurrentReader.close()
        self.Index = 0
        self.lFaccName = []
        
        
    def MoveToNextFile(self):
        if self.Index >= len(self.lFaccName):
            return False
        self.CurrentReader.close()
        print "opening fakba file [%d][%s]" %(self.Index,self.lFaccName[self.Index])
        self.CurrentReader.open(self.lFaccName[self.Index])
        self.Index += 1
        return True
        
    def ReadNext(self):
        if self.CurrentReader.empty():
            if not self.MoveToNextFile():
                return []
            
        lvCol = self.CurrentReader.ReadNextFile()
        if [] == lvCol:
            if not self.MoveToNextFile():
                return []
            lvCol = self.CurrentReader.ReadNextFile()
            
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
        lFacc = self.ReadNext()
        if [] == lFacc:
            raise StopIteration
        lRes = [facc for facc in lFacc if facc.ObjId != ""]
        return lRes
            


