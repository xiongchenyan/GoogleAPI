'''
Created on May 27, 2014

@author: cx
'''

import site

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from cxBase.base import cxBaseC,cxConf
from cxBase.WalkDirectory import WalkDir
from ObjCenter.ObjCacheCenter import ObjCacheCenterC
from GoogleFreebaseAPI.APIBase import *
from GoogleFreebaseAPI.TopicAPI  import *
import os,ntpath
class FbObjCacheCenterC(ObjCacheCenterC):
    def Init(self):
        ObjCacheCenterC.Init(self)
        self.LastObj = FbApiObjectC()
        
    
    
    def SegObjIdFromFName(self,FName):
        return FbApiObjectC.SegObjIdFromFName(ntpath.basename(FName))  
    
    def FetchObj(self,ObjId):
        if ObjId == self.LastObj.GetId():
            return self.LastObj
        
        FbApiObj = FbApiObjectC(ObjId)
        if ObjId in self.hObj: 
            FbApiObj.load(self.GetDirForObj(ObjId))
            self.LastObj = FbApiObj
            return FbApiObj
        
        FbApiObj = FetchFreebaseTopic(FbApiObj)
        if self.WriteCache:
            self.hObj[ObjId] = True
            FbApiObj.dump(self.GetDirForObj(ObjId))
        self.LastObj = FbApiObj
        return FbApiObj
   
                
        