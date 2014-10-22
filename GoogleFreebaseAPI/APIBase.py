'''
Created on Apr 4, 2014
base of API's
@author: cx
'''



APIKey = ['AIzaSyDPPpQkeRZSof6iSVLduy9ITh91Ub-CcIg','AIzaSyAspSw81ep-hspXStI4zCVt-lC-xNRD8b8']
#APIKey = ['AIzaSyAspSw81ep-hspXStI4zCVt-lC-xNRD8b8']



from copy import deepcopy
from TopicJsonTraverse import *
import json
import pickle
import sys
class FbApiObjectC(object):
    #two dict that record the raw return results from Search API and Topic API
    #only keey to hTopic?
    #and lots of different measure the extract the information from dict, and set attributes
    def Init(self):
        self.hBase = {'id':'','name':'','score':0,'notable':{}}
        self.hTopic = {}
        
        self.NotableType = ""
        self.lLinkedObj = []
        self.Desp = ""
        self.lAlias = []
        self.lType = []
        self.MaxFileNameLen = 200
        
        
    def __init__(self,Id="",name="",score = 0):
        self.Init()
        self.hBase['name'] = name
        self.hBase['mid'] = Id
        self.SetScore(score)
        
        
    def __deepcopy__(self,memo):
        APIObj = FbApiObjectC()
        APIObj.hBase = deepcopy(self.hBase,memo)
        APIObj.hTopic = deepcopy(self.hTopic,memo)
        APIObj.NotableType = deepcopy(self.NotableType,memo)
        APIObj.lLinkedObj = deepcopy(self.lLinkedObj,memo)
        APIObj.Desp = deepcopy(self.Desp,memo)
        APIObj.lAlias = deepcopy(self.lAlias,memo)
        APIObj.lType = deepcopy(self.lType,memo)
        return APIObj
    
    
    def clear(self):
        self.Init()
        
    def GetId(self):
        return self.GetBaseField('mid')
    
    def GetName(self):
        name = self.GetBaseField('name')
        if "" == name:
            name = self.GetNameViaTopic()
        try:
            name = name.encode('ascii','replace')
        except UnicodeDecodeError:
            sys.stderr.write('encode error')
            name = ""
        return name
    
    def GetScore(self):
        if '' == self.GetBaseField('score'):
            return 0
        return float(self.GetBaseField('score'))
    
    def SetScore(self,score):
        self.hBase['score'] = score
    
    def SetName(self,name):
        self.hBase['name'] = name
    
    def GetNotable(self):
        #notable may not be notable_type, could be notable_for (a object)
        if "" == self.GetBaseField('notable'):
            return {}
        return self.GetBaseField('notable')
        
    
    def GetBaseField(self,Field):
        if not Field in self.hBase:
            return ""
        return self.hBase[Field]
        
    
    
    
    #to extract from hTopic
    #required functions:
        #get all types: [type id]
        #get notable_types: id
        #get all linked object as: [edge,obj (with id,name set)]
        #get all linked values [edge,value]        ?
        #get description: text
        #get alias: [text]
    
    
    def GetNameViaTopic(self):
        lDfsRes = FreebaseTopicApiJsonDfs(self.hTopic,InitNamePath())
        name = ""
        for res in lDfsRes:
            name = res.hEnd['value']
        self.hBase['name'] = name
        return name
        
        
        
        
        
    def GetAlias(self):
        if [] != self.lAlias:
            return self.lAlias
        
        lConstrainPath = InitAliasPath()
        lDfsRes = FreebaseTopicApiJsonDfs(self.hTopic,lConstrainPath)
        
        for res in lDfsRes:
            self.lAlias.append(res.hEnd['value'].encode('ascii','ignore'))
        return self.lAlias
    
    def GetDesp(self):
        if "" != self.Desp:
            return self.Desp
        lDfsRes = FreebaseTopicApiJsonDfs(self.hTopic,InitDespPath())
        for res in lDfsRes:
            self.Desp = res.hEnd['value'].encode('ascii','ignore')
        return self.Desp
    
    def GetNotableType(self):
        if "" != self.NotableType:
            return self.NotableType
        lDfsRes = FreebaseTopicApiJsonDfs(self.hTopic,InitNotableTypePath())
        for res in lDfsRes:
            self.NotableType = res.hEnd['id'].encode('ascii','ignore')
        return self.NotableType
    
    def GetType(self,Filter = True):
        if [] == self.lType:
            lDfsRes = FreebaseTopicApiJsonDfs(self.hTopic,InitTypePath())
            for res in lDfsRes:
                self.lType.append(res.hEnd['id'].encode('ascii','ignore'))
        if Filter:
            lNew = []
            for TypeStr in self.lType:
                if TypeStr.startswith('/common'):
                    continue
                if TypeStr.startswith('/user'):
                    continue
                lNew.append(TypeStr)
            self.lType = lNew 
        return self.lType
    
    def GetNeighbor(self):
        if [] != self.lLinkedObj:
            return self.lLinkedObj
        
        lDfsRes = FreebaseTopicApiJsonDfs(self.hTopic,InitNeighborPath())
        for res in lDfsRes:
            self.lLinkedObj.append([res.lPath[0],FbApiObjectC(res.hEnd['id'],res.hEnd['text'])])
            
            
        lDfsRes = FreebaseTopicApiJsonDfs(self.hTopic,InitNeighborCompoundPath())
        for res in lDfsRes:
            path = res.lPath[3]
            self.lLinkedObj.append([path,FbApiObjectC(res.hEnd['id'],res.hEnd['text'])])
            
        return self.lLinkedObj
        
     
    #pickle dump and load
    
    def FormCategoryAttCnt(self):
        
        hCate = {}
        #go through the json dict
        #cate get from the item in self.hTopic
        #cnt is the len(hTopic[item]['values'])
        
        for item in self.hTopic:
            vCol = item.strip('/').split('/')
            if len(vCol) < 2:
                continue
            domain = '/' + vCol[0] + '/' + vCol[1]
            if 'values' in self.hTopic[item]:
                cnt = len(self.hTopic[item]['values'])
            else:
                continue
            
            if not domain in hCate:
                hCate[domain] = cnt
            else:
                hCate[domain] += cnt
        return hCate
            
                
                
         
     
    def GenerateFName(self):
        return self.GetId().replace('/','_')[:self.MaxFileNameLen]
    
    @staticmethod
    def SegObjIdFromFName(FName):
        res = '/m/' + FName[3:]
        return res
    
    
    def dump(self,OutDir):
        FName = OutDir + "/" + self.GenerateFName()
        try:
            out = open(FName,'w')
        except IOError:
            sys.stderr.write('dump obj [%s] file open failed' %(FName))
            return False
        pickle.dump(self.hBase,out)
        pickle.dump(self.hTopic,out)
        out.close()
        return True
    
    def load(self,InDir):
        FName = InDir + "/" + self.GenerateFName()
        try:
            In = open(FName,'r')
            self.hBase = pickle.load(In)
            self.hTopic = pickle.load(In)
            In.close()
        except (IOError,EOFError):
            sys.stderr.write('load obj [%s] file open failed\n' %(FName))
            return False
        return True
        
     
    @staticmethod
    def NormalizeObjRankScore(lObj):
        Total = 0.0
        for Obj in lObj:
            Total += Obj.GetScore()
            
        if Total != 0:
            for i in range(len(lObj)):
                lObj[i].hBase['score'] /= Total   
        return lObj
        
        
        
            
        
    
    