'''
Created on Apr 7, 2014
traverse the json returned by topic api
a path constrain sets how will the dfs follow
a dfs that takes json load input and output [path,id,text] as dfs result
@author: cx

the json only have three kinds:
    list of dict (list of edge to go)
    dict (edge to go)
    other (attributes)
'''



from copy import deepcopy

class PathConstrainC(object):
    
    def Init(self):
        self.hTargetEdge = {} #where I go
        self.AllEdge = False #if True then I only avoid hFilterPath
        self.hMustHaveNeighbor = {} #this dict must have exactly the same neighbor
        self.hFilterPath = {}        
        self.hEnd = {} #the end step, extract all hEnd edge's obj as results (id,text,etc)
        
    def __init__(self):
        self.Init()
        
    
    
    

class TopicApiDfsResC(object):
    def Init(self):
        self.lPath = []
        self.hEnd = {} #end att: value
    def __init__(self):
        self.Init()
        
    def deepcopy(self,memo):
        Res = TopicApiDfsResC()
        Res.lPath = deepcopy(self.lPath,memo)
        Res.hEnd = deepcopy(self.hEnd,memo)
        return Res



def InitNamePath():
    lPathConstrain = []
    node = PathConstrainC()
    node.hTargetEdge = {'/type/object/name':1}
    
    lPathConstrain.append(node)
    
    node = PathConstrainC()
    node.hTargetEdge = {'values':1}
    node.hMustHaveNeighbor = {'valuetype','string'}    
    lPathConstrain.append(node)
    
    node = PathConstrainC()
    node.hEnd = {'value':""}
    node.hMustHaveNeighbor={'lang','en'}    
    lPathConstrain.append(node)
    return lPathConstrain


def InitDespPath():
    lPathConstrain = []
    node = PathConstrainC()
    node.hTargetEdge = {'/common/topic/description':1}
    
    lPathConstrain.append(node)
    
    node = PathConstrainC()
    node.hTargetEdge = {'values':1}
    node.hMustHaveNeighbor = {'valuetype','string'}    
    lPathConstrain.append(node)
    
    node = PathConstrainC()
    node.hEnd = {'value':""}
    node.hMustHaveNeighbor={'lang','en'}    
    lPathConstrain.append(node)
    return lPathConstrain

def InitNotableTypePath():  
    lPathConstrain = []
    node = PathConstrainC()
    node.hTargetEdge = {'/common/topic/notable_types':1}
    
    lPathConstrain.append(node)
    
    node = PathConstrainC()
    node.hTargetEdge = {'values':1}
    node.hMustHaveNeighbor = {'valuetype','object'}    
    lPathConstrain.append(node)
    
    node = PathConstrainC()
    node.hEnd = {'id':""}
    node.hMustHaveNeighbor={'lang','en'}    
    lPathConstrain.append(node)
    return lPathConstrain  


def InitAliasPath():  
    lPathConstrain = []
    node = PathConstrainC()
    node.hTargetEdge = {'/common/topic/alias':1}
    
    lPathConstrain.append(node)
    
    node = PathConstrainC()
    node.hTargetEdge = {'values':1}
    node.hMustHaveNeighbor = {'valuetype','string'}    
    lPathConstrain.append(node)
    
    node = PathConstrainC()
    node.hEnd = {'value':""}
    node.hMustHaveNeighbor={'lang','en'}    
    lPathConstrain.append(node)
    return lPathConstrain  

def InitTypePath():
    lPathConstrain = []
    node = PathConstrainC()
    node.hTargetEdge = {'/type/object/type':1}
    
    lPathConstrain.append(node)
    
    node = PathConstrainC()
    node.hTargetEdge = {'values':1}
    node.hMustHaveNeighbor = {'valuetype','object'}    
    lPathConstrain.append(node)
    
    node = PathConstrainC()
    node.hEnd = {'id':""}
    node.hMustHaveNeighbor={'lang','en'}    
    lPathConstrain.append(node)
    return lPathConstrain  

def InitNeighborPath():
    lPathConstrain = []
    node = PathConstrainC()
    node.AllEdge = True
    node.hFilterPath = dict(zip(['/common','/type'],range(2)))
    
    lPathConstrain.append(node)
    
    node = PathConstrainC()
    node.hTargetEdge = {'values':1}
    node.hMustHaveNeighbor = {'valuetype','object'}    
    lPathConstrain.append(node)
    
    node = PathConstrainC()
    node.hEnd = {'id':"",'text':''}
    node.hMustHaveNeighbor={'lang','en'}
    lPathConstrain.append(node)
    return lPathConstrain

def InitNeighborCompoundPath():
    lPathConstrain = []
    node = PathConstrainC()
    node.AllEdge = True
    node.hFilterPath = dict(zip(['/common','/type'],range(2)))
    
    lPathConstrain.append(node)
    
    node = PathConstrainC()
    node.hTargetEdge = {'values':1}
    node.hMustHaveNeighbor = {'valuetype','compound'}    
    lPathConstrain.append(node)
    
    
    node = PathConstrainC()
    node.hTargetEdge = {'property':1}
    lPathConstrain.append(node)
    
    node = PathConstrainC()
    node.AllEdge = True
    node.hFilterPath = dict(zip(['/common','/type'],range(2)))
    
    lPathConstrain.append(node)
    
    
    node = PathConstrainC()
    node.hTargetEdge = {'values':1}
    node.hMustHaveNeighbor = {'valuetype','object'}    
    lPathConstrain.append(node)
    
    node = PathConstrainC()
    node.hEnd = {'id':"",'text':''}
    node.hMustHaveNeighbor={'lang':'en'}
    lPathConstrain.append(node)
    
    return lPathConstrain





def FreebaseTopicApiJsonDfs(hCurrentTopicDict,lPathConstrain,lCurrentPath=[],level = 0):
    lDfsRes = []
    CurrentConstrain = lPathConstrain[level]
    #if need end
        #keep all value in hEnd
        #return [TopicApiDfsResC]
        
    if CurrentConstrain.hEnd != {}:
        DfsRes = TopicApiDfsResC()
        DfsRes.lPath = list(lCurrentPath)
        DfsRes.hEnd = dict(CurrentConstrain.hEnd)
        for item in DfsRes.hEnd:
            if item in hCurrentTopicDict:
                DfsRes.hEnd[item] = hCurrentTopicDict[item]
        lDfsRes.append(DfsRes)
        
        
    if level == len(lPathConstrain) - 1:
        return lDfsRes     
    
    #walk along hCurrentTopicDict's edge according to lPathConstrain
        #update lCurrentPath and level, and hCurrentTopicDict, call next level
        #collect next value's result, extend to lDfsRes
    #return
    
    
    #check if this dict correct
    
    for item in CurrentConstrain.hMustHaveNeighbor:
        if not item in hCurrentTopicDict:
            return []
        if hCurrentTopicDict[item] != CurrentConstrain.hMustHaveNeighbor[item]:
            return []
    
    #for each target path, call dfs, collect result
    
    for item in hCurrentTopicDict:
        if (not item in CurrentConstrain.hTargetEdge) &(not CurrentConstrain.AllEdge):
            continue
        if item in CurrentConstrain.hFilterPath:
            continue
        NextData = hCurrentTopicDict[item]
        if type(NextData) == dict:
            NextData = [NextData]
        if not type(NextData) == list:
            continue
        for hNextDict in NextData:
            lDfsRes.extend(FreebaseTopicApiJsonDfs(hNextDict,
                                                   lPathConstrain,
                                                   list(lCurrentPath + [item]),
                                                   level + 1
                                                   ))   
    
    return lDfsRes
