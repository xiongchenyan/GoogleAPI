'''
Created on Dec 17, 2014 5:38:50 PM
@author: cx

what I do:
map OhsumedDocNo to MeSH term and their UI
what's my input:
doc no + preformed dict
what's my output:
its annotated MeSH term


I also formulate such dict
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
import pickle

from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from cxBase.TextBase import TextBaseC
from MeSHBase.MeSHTermCenter import MeSHTermCenterC

class OhsumedDocMeSHAnaCenterC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.DocMeSHDictName = ""
        self.hDocToMeSh = {}   #DocNo => [[UI,term]], formulated, and loaded for use
    
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.DocMeSHDictName = self.conf.GetConf('docmeshdict')
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'docmeshdict'
        
        
    def FetchMeSH(self,DocNo):
        if {} == self.hDocToMeSh:
            if "" != self.DocMeSHDictName:
                self.hDocToMeSh = pickle.load(open(self.DocMeSHDictName))
        if DocNo in self.hDocToMeSh:
            return self.hDocToMeSh[DocNo]
        return []
    
    
    def FormDocMeSHDict(self,DocInName,MeSHTermDictIn,hTargetDocNo = {}):
        MeSHTermCenter = MeSHTermCenterC()
        MeSHTermCenter.DictDumpPath = MeSHTermDictIn
        
        lLine = []
        cnt = 0
        for line in open(DocInName):
            line = line.strip()
            if '.I' == line[:2]:
                DocNo,lTerm = self.SegDocMeSHAna(lLine)
                if {} != hTargetDocNo:
                    if not DocNo in hTargetDocNo:
                        continue
                lLine = []
                lTermWithUI = []
                for term in lTerm:
                    UI = MeSHTermCenter.MapTerm(term)
                    if UI == "":
                        print "annotated term [%s] not find" %(term)
                        continue
                    lTermWithUI.append([UI,term])
                self.hDocToMeSh[DocNo] = lTermWithUI
                cnt += 1
                if 0 == (cnt % 1000):
                    print "[%d] doc finished" %(cnt)
            lLine.append(line)
        print "dict made"
        return
                    
                    
                    
                    
    def SegDocMeSHAna(self,lLine):
        DocNo = ""
        lTerm = []
        for i in range(1,len(lLine)):
            if lLine[i-1] == '.U':
                DocNo = lLine[i]
            if lLine[i-1] == '.M':
                lTerm = lLine[i].split(';')
                lTerm = [TextBaseC.RawClean(term) for term in lTerm]
        return DocNo,lTerm
                
    
    

