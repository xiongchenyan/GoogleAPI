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
        
    
