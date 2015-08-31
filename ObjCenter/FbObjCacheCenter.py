'''
Created on May 27, 2014

@author: cx
'''

'''
Aug 30 2015:
Major update:
    In case the Freebase API may not be supported by Google in the near feature,
    Add function that fetch FbObj from that made from Fb dumps
        while no longer use TopicAPI to fetch objects
things changed here:
    FetchObj use FbObjC (new class that support same function with FbAPIObj, but more clean to use, and is forged from fb dumps),
     instead of FbAPIObj
     
    check whether the object in dump by whether the file exists, not by a preloaded dict (no need)
    if not exist, throw an exception, ask for preparations using 'Fetch Fb Obj From dump' 
     
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
        if ObjId == 'query':
            return FbApiObj
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
   
                
        