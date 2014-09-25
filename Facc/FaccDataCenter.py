'''
Created on Sep 25, 2014
the data center for Facc annotations:
in: Facc Dir, one facc file for one query, prepared by MakeFaccForQuery.py
do: given a query, return all  its facc docs in FaccForDocC 
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from Facc.FaccDoc import *
from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
from cxBase.WalkDirectory import WalkDir
class FaccDataCenterC(cxBaseC):
    
    def Init(self):
        self.FaccDir = ""
        
    def SetConf(self,ConfIn):
        conf = cxConfC(ConfIn)
        self.FaccDir = conf.GetConf('faccdir')
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print "faccdir"
        
        
    def FetchFaccForQ(self,query):
        FName = self.FaccDir + '/' + query
        lFaccDoc = FaccForDocC().ReadFaccDocs(FName)
        return lFaccDoc
    
    
    def FetchAllAnnotation(self):
        hDocObj = {}  #doc"\t"objid -< facc score (mostly <0.99 though)
        
        
        #go through all files in the directory 
        lFName = WalkDir(self.FaccDir)
        for fname in lFName:
            lFaccDoc = FaccForDocC().ReadFaccDocs(fname)
            for FaccDoc in lFaccDoc:
                DocNo = FaccDoc.DocNo
                for FaccAna in FaccDoc.lFacc:
                    ObjId = FaccAna.ObjId
                    score = FaccAna.Prob
                    hDocObj[DocNo + '\t' + ObjId] = score
        return hDocObj
                    
                
    
