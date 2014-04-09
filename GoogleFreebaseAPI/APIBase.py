'''
Created on Apr 4, 2014
base of API's
@author: cx
'''



APIKey = ['AIzaSyDPPpQkeRZSof6iSVLduy9ITh91Ub-CcIg']




from copy import deepcopy
from TopicJsonTraverse import *
import json
import pickle

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
        
        
    def __init__(self,Id="",name=""):
        self.Init()
        self.hBase['name'] = name
        self.hBase['mid'] = Id
        
        
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
        
        
    def GetId(self):
        return self.GetBaseField('mid')
    
    def GetName(self):
        name = self.GetBaseField('name')
        if "" == name:
            return self.GetNameViaTopic()
        return name
    
    def GetScore(self):
        if '' == self.GetBaseField('score'):
            return 0
        return float(self.GetBaseField('score'))
    
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
            self.lAlias.append(res.hEnd['value'].encode('ascii','replace'))
        return self.lAlias
    
    def GetDesp(self):
        if "" != self.Desp:
            return self.Desp
        lDfsRes = FreebaseTopicApiJsonDfs(self.hTopic,InitDespPath())
        for res in lDfsRes:
            self.Desp = res.hEnd['value'].encode('ascii','replace')
        return self.Desp
    
    def GetNotableType(self):
        if "" != self.NotableType:
            return self.NotableType
        lDfsRes = FreebaseTopicApiJsonDfs(self.hTopic,InitNotableTypePath())
        for res in lDfsRes:
            self.NotableType = res.hEnd['id'].encode('ascii','replace')
        return self.NotableType
    
    def GetType(self):
        if [] != self.lType:
            return self.lType
        lDfsRes = FreebaseTopicApiJsonDfs(self.hTopic,InitTypePath())
        for res in lDfsRes:
            self.lType.append(res.hEnd['id'].encode('ascii','replace'))
        return self.lType
    
    def GetNeighbor(self):
        if [] != self.lLinkedObj:
            return self.lLinkedObj
        
        lDfsRes = FreebaseTopicApiJsonDfs(self.hTopic,InitNeighborPath())
        for res in lDfsRes:
            self.lLinkedObj.append([json.dumps(res.lPath),FbApiObjectC(res.hEnd['id'],res.hEnd['text'])])
            
            
        lDfsRes = FreebaseTopicApiJsonDfs(self.hTopic,InitNeighborCompoundPath())
        for res in lDfsRes:
            lPath = res.lPath[3:]
            self.lLinkedObj.append([json.dumps(lPath),FbApiObjectC(res.hEnd['id'],res.hEnd['text'])])
            
        return self.lLinkedObj
        
     
    #pickle dump and load
     
    def GenerateFName(self):
        return self.GetId().replace('/','_')
    
    def dump(self,OutDir):
        out = open(OutDir + "/" + self.GenerateFName(),'w')
        pickle.dump(self.hBase,out)
        pickle.dump(self.hTopic,out)
        out.close()
        return True
    
    def load(self,InDir):
        In = open(InDir + "/" + self.GenerateFName(),'r')
        self.hBase = pickle.load(In)
        self.hTopic = pickle.load(In)
        In.close()
        return True
        
     
        
        
        
        
            
        
    
    