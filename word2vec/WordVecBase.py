'''
Created on May 6, 2014

@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from operator import itemgetter
from cxBase.base import cxConf
from cxBase.Vector import VectorC
from cxBase.KeyFileReader import KeyFileReaderC
import ntpath
class Word2VecC(VectorC):
    def Init(self):
        VectorC.Init(self)
        self.word = ""
        
    def __init__(self,InData={},word = ""):
        VectorC.__init__(InData)
        self.word = word
        if type(InData) == str:
            self.SetLine(InData)
        
    
    def SetLine(self,line):
        word,vec = line.strip().split('\t')
        vec = [float(col) for col in vec.split()]
        self.hDim = dict(zip(vec,range(len(vec))))
        self.word = word
        return True
    
    
    def Key(self):
        return self.word
    
    def dumps(self):
        res = self.word + "\t" + " ".join([str(item) for key,item in sorted(self.hDim.items(),key=itemgetter(0))])
        return res
    def loads(self,line):
        self.SetLine(line)
    
    def load(self,InName):
        try:
            for line in open(InName):
                self.SetLine(line)
                return True
        except IOError:
            return False
    
    def OutName(self):
        return self.word.replace('/','_')
    def SegIdFromName(self,OutName):
        return ntpath.basename(OutName).replace('_','/')
    
    
    def clear(self):
        self.word = ""
        self.hDim.clear()
    def empty(self):
        if (self.word == "") & ({} == self.hDim):
            return True
        
class Word2VecReaderC(KeyFileReaderC):
    def ReadNextKey(self):
        lvCol = super(Word2VecReaderC,self).ReadNextKey()
        WordVec = Word2VecC('\t'.join(lvCol[0]))
        return WordVec
        