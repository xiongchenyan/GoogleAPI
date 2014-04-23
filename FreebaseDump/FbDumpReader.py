'''
Created on Apr 21, 2014
read freebase dump
once an object's all triples
cut off at a limited amount of lines
@author: cx
'''


import site
site.addsitedir("/bos/usr0/cx/PyCode/cxPyLib")

from FbDumpBasic import *
import gzip
from cxBase.KeyFileReader import *

class FbDumpReaderC(KeyFileReaderC):
    
    
    def Init(self):
        super(FbDumpReaderC,self).Init()
        self.UseGzip = True #always
    
            
    def ReadNextKey(self):
        lvCol = super(FbDumpReaderC,self).ReadNextKey()
        lvCol = [self.ProcessOneLine(vCol) for vCol in lvCol]
        return lvCol
        
    def ProcessOneLine(self,vCol):
        if len(vCol) < 3:
            return []
        vCol = [DiscardPrefix(col) for col in vCol[:3]]      
        return vCol
        
    
    
    
    
    