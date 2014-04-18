'''
Created on Apr 7, 2014
given a query, bfs it in Freebase
query -> (search) -> object
object->(neighbor) -> object (cnt as length 1)
object ->(type) -> object( cnt as length 1 as well...)

output:
a path file:
    query's objects (list of ids) edge (search
    object object edge
object details, one per file

parameters:
query
Out directory: (query_bfs, + obj/object details)
level of BFS
constrains:
    max # of searched object for query
    max # of co-type expansion
    max # of neighbor expansion
    (thus the bfs will be able to be re-do by output data very quickly in memory)
@author: cx
'''



import site
import os
import pickle
import json
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib/')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI/')
from cxBase.base import cxConf,cxBaseC
from APIBase import *
from MQLAPI import *
from SearchAPI import *
from TopicAPI import *

class BfsQueryFreebaseC(cxBaseC):
    def Init(self):
        self.ObjectCashDir = '' #dir used to cash object
        self.hEdges = {} #bfs edges
        self.hSeenObj = {} #all obj seen
        self.WorkDir = ""
        
        self.BFSLvl = 2
        self.MaxSearchRes = 5
        self.MaxCoTypeExp = 100
        self.MaxNeighborExp = 100
        
        return
    
    @staticmethod
    def ShowConf():
        print "workdir\nbfslvl\nmaxsearchres\nmaxcotypeexp\nmaxneighborexp"
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.WorkDir = conf.GetConf('workdir')
        self.ObjectCashDir = self.WorkDir + "/obj"
        if not os.path.isdir(self.ObjectCashDir):
            os.makedirs(self.ObjectCashDir)
        
        self.BFSLvl = int(conf.GetConf('bfslvl',self.BFSLvl))
        self.MaxSearchRes = int(conf.GetConf('maxsearchres',self.MaxSearchRes))
        self.MaxCoTypeExp = int(conf.GetConf('maxcotypeexp',self.MaxCoTypeExp))
        self.MaxNeighborExp = int(conf.GetConf('maxneighborexp',self.MaxNeighborExp))
        
        self.load()
        return True
    
    
    def load(self):
        #try to load dumped result in workdir, if exist
        if os.path.isfile(self.EdgeDumpName()):
            In = open(self.EdgeDumpName(),'rb')
            self.hEdges = pickle.load(In)
            In.close()
        if os.path.isfile(self.ObjListName()):
            In = open(self.ObjListName(),'rb')
            self.hSeenObj = pickle.load(In) 
            In.close()          

    def dump(self):
        out = open(self.EdgeDumpName(),'wb')
        pickle.dump(self.hEdges,out)
        out.close()
        
        out = open(self.ObjListName(),'wb')
        pickle.dump(self.hSeenObj,out)
        out.close()
        return True
    
    def EdgeDumpName(self):
        return self.WorkDir + "/edgedump"
    def ObjListName(self):
        return self.WorkDir + "/objdump"
    
        
    
    
    def SearchQueryForInitObj(self,query):
        #if query in hEdges, then use dump
        #else run SearchAPI and get a list of objects
        #return a list of object, full filled
            #do the full fill because when using cash, need to load the object        
        lLinkObj = []
        
        if query in self.hEdges:
            print "query [%s] in edge cash" %(query)
            lLinkObj = [[item[0],FbApiObjectC(item[1],'')] for item in self.hEdges[query]]
            
        else:
            lObj = SearchFreebase(query)[:self.MaxSearchRes]
            lLinkObj = [['search',Obj] for Obj in lObj] 
            self.hEdges[query] = [['search',Obj.GetId()] for Obj in lObj]
            
        lLinkObj = [[item[0],self.FillObj(item[1])] for item in lLinkObj]         
        
        return lLinkObj
    
    
    def FillObj(self,FbObj):
        if FbObj.hTopic != {}:
            #filled
            return FbObj
        if FbObj.GetId() in self.hSeenObj:
            print "obj [%s] dumped to dict already" %(FbObj.GetId())
            FbObj.load(self.ObjectCashDir)
            return FbObj
        self.hSeenObj[FbObj.GetId()] = True
        FbObj = FetchFreebaseTopic(FbObj)
        FbObj.dump(self.ObjectCashDir)
        return FbObj
    
      
    
    def ExpandObjNeighbor(self,FbObj):
        #return a list of object, full filled 
        lNeighborObj = []
        
        #check if this obj id in hEdge
            #Y: get all edges, discard type edge, and extract neighbor ids
        if FbObj.GetId() in self.hEdges:    
            print "obj [%s] in edge cash" %(FbObj.GetId())        
            lNeighborObj = [[item[0],item[1]] for item in self.hEdges[FbObj.GetId()][:self.MaxNeighborExp]]
        
        #FbObj is a filled one.
            #call function of FbObj to expanded to lNeighborObj
            #add edge-> id to hEdge[FbObj.GetId()]
        else:
            lNeighborObj = [[item[0], item[1].GetId()] for item in deepcopy(FbObj.GetNeighbor())[:self.MaxNeighborExp]]
            self.hEdges[FbObj.GetId()] = list(lNeighborObj)
        
        
        return lNeighborObj
    
    
    def ExpandTypeNeighbor(self,FbObj):
        #only expand notable type for now
        #return obj are full filled
        lCoTypeObj = []
        NotableType = FbObj.GetNotableType()
        if "" == NotableType:
            return []
        if  NotableType in self.hEdges:     
            print "Type [%s]  in edge cash" %(NotableType)        
            lCoTypeObj = [[item[0],item[1]]
                          for item in self.hEdges[NotableType][:self.MaxCoTypeExp]]
        
        else:
            #get notable type
            #call MQL API to get instance ids
            #constract cotype obj from id
            #add cotype_typename,cotype id to hedge
            lCoTypeId = FetchTypeInstance(NotableType,self.MaxCoTypeExp)
            lCoTypeObj = [['cotype/'+NotableType,objid] for objid in lCoTypeId]
            self.hEdges[NotableType] = list(lCoTypeObj)
        return lCoTypeObj
    
    
    def BFS(self,qid,query):
        #typical bfs
        #initial que by query-search
        #keep que [path,obj] (path is [edge1,edge2] etc
        #for each obj in que
            #call PerObjProcess() to deal with the obj and edge (API left for sub class)
            #if lvl (len(path)) < self.BFSLVL, then expand this node via
                #Neighbor Obj
                #TypeNeighbor Obj
                
        #only keep the edge and obj id in que
        #only when working on this obj, then fill it
        #dump after a while
        
        print "working on query [%s]" %(query)
        
        lSearchObj = []
        if True:
            lSubQ = FormEnumeratePhraseQuery(query)
            print "to query sub queries [%s]" %(json.dumps(lSubQ))
            for q in lSubQ:
                lSearchObj.extend(self.SearchQueryForInitObj(q))
        
        else:
            lSearchObj = self.SearchQueryForInitObj(query)
        BFSQue = [[[item[0]],item[1].GetId()] for item in lSearchObj]
        
        print "start nodes [%d]:" %(len(BFSQue)) 
        for node in BFSQue:
            print "%s\t[%s]" %(json.dumps(node[0]), node[1])
        
        p = 0
        DumpCnt = 0
        DumpFre = 5000
        while p < len(BFSQue):
            edge,CurrentObjId = BFSQue[p]
            CurrentObj = FbApiObjectC(CurrentObjId,"")
            CurrentObj = self.FillObj(CurrentObj)
            print 'now obj [%s] - [%s][%s]' %(json.dumps(edge),
                                              CurrentObj.GetId().encode('utf-8','ignore'),
                                       CurrentObj.GetName().encode('utf-8','ignore'))
            p += 1
            self.ProcessPerObj(edge,CurrentObj,qid,query)
            
            if len(edge) >= self.BFSLvl:
                continue
            lNeighborObjId = self.ExpandObjNeighbor(CurrentObj)
            lCoTypeObjId = self.ExpandTypeNeighbor(CurrentObj)
            
            lToAdd = [[list(edge + [item[0]]), item[1]] for item in lNeighborObjId+lCoTypeObjId]
            
            print 'add [%d] node from neighbor\nadd [%d] node from co type' %(len(lNeighborObjId),len(lCoTypeObjId))
            BFSQue.extend(lToAdd)          
            print 'bfs que size [%d] at [%d]' %(len(BFSQue),p)
            
            if len(BFSQue) / DumpFre > DumpCnt:
                self.dump()
                print "dumping for [%d] time" %(DumpCnt)
                DumpCnt = len(BFSQue) / DumpFre
            
        print "bfs finished, total meet [%d] objects" %(len(BFSQue))
        return True
    
    def ProcessPerObj(self,lPath,FbObj,qid,query):
        #api left for sub class to process a bfs'd result. like vote up a term in FbObj's name
        print "get obj[%s][%s] via [%s]" %(FbObj.GetId(),FbObj.GetName(),json.dumps(lPath))
        return True
    
      
        
def BfsQueryFreebaseUnitRun(ConfIn):
    conf = cxConf(ConfIn)
    InName = conf.GetConf('in')
    BFSer = BfsQueryFreebaseC(ConfIn)
    
    for line in open(InName):
        qid,query = line.strip().split('\t')
        BFSer.BFS(qid,query)
    BFSer.dump()
    return True
        
        

def FormEnumeratePhraseQuery(query):
    lSubQ = []
    lTerm = query.split()
    if len(lTerm) == 1:
        return [query]
    
    LenSt = 2
    LenEd = len(lTerm)
    for CurLen in range(LenSt,LenEd + 1):
        for st in range(len(lTerm) - CurLen + 1):
            ThisQ = ' '.join(lTerm[st:st + CurLen])
            if not ThisQ in lSubQ:
                lSubQ.append(ThisQ)
    return lSubQ

