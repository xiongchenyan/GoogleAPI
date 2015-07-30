'''
Created on Dec 19, 2014 11:28:33 AM
@author: cx

what I do:
the root class of 
FbObjCacheCenterC
MeSHObjCacheCenterC (TBD)

main function is to provide different fields for a obj, looking up by id
I actively keep and update a cache directory to facilitate the look up process 
what's my input:
obj id
what's my output:
target fields, as required

'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from cxBase.base import cxBaseC,cxConf
from cxBase.WalkDirectory import WalkDir
import os,ntpath,sys
class ObjCacheCenterC(cxBaseC):
    def Init(self):
        self.WorkDir = ""
        self.WriteCache = True
        self.hObj = {}
        self.LastObj = ""    #to be defined by subclasses
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.WorkDir = conf.GetConf('objcachedir') + '/'
        print "set obj cachedir to [%s]" %(self.WorkDir)
        self.WriteCache = bool(int(conf.GetConf('writecache',self.WriteCache)))
        self.CreateHash()
        return True
    
    @classmethod
    def ShowConf(cls):
        print cls.__name__
        print "objcachedir\nwritecache"
        
    
    def GetDirForObj(self,ObjId):
        #create a 2 level directory for ObjId
        vCol = ObjId.strip('/').split('/')
        if len(vCol) < 2:
            print "ObjId [%s] format error"
            sys.exit()
        mid = vCol[1]
        OneDir = mid[0]
        TwoDir = mid[1]
        res = self.WorkDir + "/%s/%s/" %(OneDir,TwoDir)
#         print "caching obj to [%s][%s]" %(self.WorkDir,res)
        if not os.path.isdir(res):
            os.makedirs(res)
        return res
    
    def CreateHash(self):
        lFName = WalkDir(self.WorkDir)
        for FName in lFName:
            ObjId = self.SegObjIdFromFName(FName)
            self.hObj[ObjId] = True
        print "total [%d] obj in [%s]" %(len(self.hObj),self.WorkDir)
        return True
    
    def SegObjIdFromFName(self,FName):
        return ntpath.basename(FName)
    
    
    def FetchObj(self,ObjId):
        print "call my subclass"
        return
        
    
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
    
    
    
        
                
        
