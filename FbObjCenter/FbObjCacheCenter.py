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
        self.LastObj = FbApiObjectC()
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.WorkDir = conf.GetConf('objcachedir')
        self.WriteCache = bool(int(conf.GetConf('writecache',self.WriteCache)))
        self.CreateHash()
        return True
    
    @staticmethod
    def ShowConf():
        print "objcachedir\nwritecache"
        
    
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
            ObjId = FbApiObjectC.SegObjIdFromFName(ntpath.basename(FName))
            self.hObj[ObjId] = True
        print "total [%d] obj in [%s]" %(len(self.hObj),self.WorkDir)
        return True
    
    
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
        
    
    def FetchObjField(self,ObjId,field):
        return self.FetchObj(ObjId).GetField(field)
    
    def FetchObjDesp(self,ObjId):
        return self.FetchObjField(ObjId, 'Desp')
    
    def FetchObjName(self,ObjId):
        return self.FetchObjField(ObjId, 'Name')
    
    def FetchObjNotableType(self,ObjId):
        return self.FetchObjField(ObjId, 'NotableType')
    
    def FetchObjType(self,ObjId):
        return self.FetchObjField(ObjId, 'Type')
    
    def FetchObjAlias(self,ObjId):
        return self.FetchObjField(ObjId, 'Alias')
    
    def FetchObjNeighbor(self,ObjId):
        '''
        return a list,
            each item: item[0] path, item[1] FbApiObjectC()
        '''
        return self.FetchObjField(ObjId, 'Neighbor')
    
    
    
        
                
        