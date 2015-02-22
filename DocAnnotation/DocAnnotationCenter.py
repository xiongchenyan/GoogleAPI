'''
Created on Dec 22, 2014 3:49:27 PM
@author: cx

what I do:
I am the base class for document annotations
Main goal:
    add doc.lAnnotation for IndriBaseDocC
what's my input:
A path for doc->lAna[objid,name,score] dict
   maybe only have objid,name, then add default score: 1
what's my output:
doc add lAnnotation

'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
import pickle

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC

class DocAnnotationCenterC(cxBaseC):
    def Init(self):
        self.hDocAna = {}
        self.DictPath = ""
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.DictPath = self.conf.GetConf('docanadict')
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'docanadict'    
    
    def AddDefaultAnaScore(self):
        for key,lAna in self.hDocAna.items():
            for i in range(len(lAna)):
                if len(lAna[i]) == 2:
                    lAna[i].append(1)
            self.hDocAna[key] = lAna
        
            
                    
        
    def FillDoc(self,doc):
        if {} == self.hDocAna:
            if "" != self.DictPath:
                print "loading docanadict from [%s]" %(self.DictPath)
                self.hDocAna = pickle.load(open(self.DictPath))
                self.AddDefaultAnaScore()
                print "doc ana dict prepared"
                
        DocNo = doc.DocNo
        if DocNo in self.hDocAna:
            doc.lAnnotation = self.hDocAna[DocNo]
        return doc
            
                



