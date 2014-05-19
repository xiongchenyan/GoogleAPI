'''
Created on May 19, 2014
input: query, facc dir, query search cache dir
output: a facc doc dir. each file for each query, all its search res's facc annotations
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from cxBase.base import cxBaseC,cxConf
from IndriRelate.IndriPackedRes import *
from Facc.FaccBase import *
from Facc.FaccReader import *

class FaccDocMakerC(cxBaseC):
    def Init(self):
        self.CashDir = ""
        self.QueryIn = ""
        self.FaccDir = ""
        self.OutDir = ""
        self.SERPDepth = 50
        self.hDocFacc = {}
        self.hTargetDocNo = {}
    @staticmethod
    def ShowConf():
        print "cashdir\nin\noutdir\nfaccdir\nserpdepth 50"
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.CashDir = conf.GetConf('cashdir')
        self.QueryIn = conf.GetConf('in')
        self.FaccDir = conf.GetConf('faccdir')
        self.OutDir = conf.GetConf('outdir')
        self.SERPDepth = int(conf.GetConf('serpdepth',self.SERPDepth))
        
    
    def LoadTargetDocNo(self):
        for line in open(self.QueryIn):
            query = line.strip().split('\t')[1]
            lDoc = ReadPackedIndriRes(self.CashDir + "/" + query)
            for Doc in lDoc:
                self.hTargetDocNo[Doc.DocNo] = True
        print "total [%d] doc to fetch facc" %(len(self.hTargetDocNo))
        return True
    
    def FetchFaccForTargetDoc(self):
        Reader = FaccReaderC()
        Reader.opendir(self.FaccDir)
        
        for lFacc in Reader:
            DocNo = lFacc[0].DocNo
            if DocNo in self.hTargetDocNo:
                print "get facc for [%s]" %(DocNo)
                self.hDocFacc[DocNo] = FaccForDocC(lFacc) 
        print "total [%d]/[%d] doc has facc" %(len(self.hDocFacc),len(self.hTargetDocNo))
        return True
    
    
    def WriteDocFacc(self):
        for line in open(self.QueryIn):
            query = line.strip().split('\t')[1]
            print "writing for q [%s]" %(query)
            lDoc = ReadPackedIndriRes(self.CashDir + "/" + query)
            OutName = self.OutDir + '/' + query
            lFaccDoc = []
            for Doc in lDoc:
                DocNo = Doc.DocNo
                if not DocNo in self.hDocFacc:
                    continue
                lFaccDoc.append(self.hDocFacc[DocNo])
            FaccForDocC.DumpFaccDocs(lFaccDoc, OutName)   
            print "q [%s] dumped [%d] facc doc" %(query,len(lFaccDoc))
        return True
    
    def Process(self):
        self.LoadTargetDocNo()
        self.FetchFaccForTargetDoc()
        self.WriteDocFacc()
        return True     
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
