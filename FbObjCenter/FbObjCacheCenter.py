'''
Created on May 27, 2014

@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from cxBase.base import cxBaseC,cxConf
from cxBase.WalkDirectory import WalkDir
from GoogleFreebaseAPI.APIBase import *
from GoogleFreebaseAPI.TopicAPI  import *
import os,ntpath
class FbObjCacheCenterC(cxBaseC):
    def Init(self):
        self.WorkDir = ""
        self.WriteCache = True
        self.hObj = {}
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.WorkDir = conf.GetConf('workdir')
        self.WriteCache = bool(conf.GetConf('writecache',self.WriteCache))
        self.CreateHash()
        return True
    
    @staticmethod
    def ShowConf():
        print "workdir\nwritecache"
        
    
    def GetDirForObj(self,ObjId):
        #create a 2 level directory for ObjId
        vCol = ObjId.strip('/').split('/')
        mid = vCol[1]
        OneDir = mid[0]
        TwoDir = mid[1]
        res = self.WorkDir + "/%s/%s/" %(OneDir,TwoDir)
        if not os.path.isdir(res):
            os.makedirs(res)
        return res
    
    def CreateHash(self):
        lFName = WalkDir(self.WorkDir)
        for FName in lFName:
            ObjId = ntpath.basename(FName).replace('_','/')
            self.hObj[ObjId] = True
        print "total [%d] obj in [%s]" %(len(self.hObj),self.WorkDir)
        return True
    
    
    def FetchObj(self,ObjId):
        FbApiObj = FbApiObjectC(ObjId)
        if ObjId in self.hObj: 
            FbApiObj.load(self.GetDirForObj(ObjId))
            return FbApiObj
        
        FbApiObj = FetchFreebaseTopic(FbApiObj)
        if self.WriteCache:
            self.hObj[ObjId] = True
            FbApiObj.dump(self.GetDirForObj(ObjId))
        return FbApiObj
        
    
            
        