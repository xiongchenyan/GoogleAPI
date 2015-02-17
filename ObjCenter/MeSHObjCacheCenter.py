'''
Created on Dec 19, 2014 5:03:00 PM
@author: cx

what I do:
I am a sub class of ObjCacheCenter

Currently:
    load pregenerated ID->MeSHTerm hBase 
    and fetch obj now is just a dict look up
what's my input:

what's my output:


'''
'''
Feb 17 2015: (to support MeSH Annotation features in Obj-doc)
Add neighbor fields in MeShTermDict
    pre read from MeSHEdge data, form neighbor dict
        Neighbor field format needs to be consistant with Fb's
    for each MeSH term, fetch its neighbors in MeSH Dict, add to its hBase{}
    And dump to dict
        (check how to pickle dump class?) (OMG I can just do it?)
Modify the pickle dump from hBase to MeSHTermC() directly, 
    thus the loaded dict directly contains the MeSHTermC()
'''


import site

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from cxBase.base import cxBaseC,cxConf
from ObjCenter.ObjCacheCenter import ObjCacheCenterC
from cxBase.KeyFileReader import KeyFileReaderC
from MeSHBase.MeSHTerm import MeSHTermC
import ntpath
import pickle
import sys
class MeSHObjCacheCenterC(ObjCacheCenterC):
    def Init(self):
        ObjCacheCenterC.Init(self)
        self.hMeSH = {}  #id -> MeSHTerm hBase
        self.MeSHTermDictIn = ""
        
    def SetConf(self, ConfIn):
        ObjCacheCenterC.SetConf(self, ConfIn)
        self.MeSHTermDictIn = self.WorkDir + 'meshtermdict'
        
        
    
    def FormMeSHTermDict(self,RawMeSHInName,MeSHEdgeInName):
        '''
        generate the MeSHTerm dict
        load each record
            seg to MeSHTermC
            add hBase to hMeSH
        Feb 17:
        load mesh edge, all edges for each record are grouped together.
            make its neighbor formats
            add to its MeSHTerm's fields
        dump
        '''
        
        cnt = 0
        lLine = []
        for line in open(RawMeSHInName):
            line = line.strip()
            if line == '*NEWRECORD':
                MeSHTerm = MeSHTermC()
                MeSHTerm.SegFromRawLines(lLine)
                self.hMeSH[MeSHTerm.GetField('id')] = MeSHTerm
                cnt += 1
                if 0 == (cnt % 100):
                    print "generating dict, processed [%d] term" %(cnt)
                lLine = []
            lLine.append(line)
        MeSHTerm = MeSHTermC()
        MeSHTerm.SegFromRawLines(lLine)
        self.hMeSH[MeSHTerm.GetField('id')] = MeSHTerm
        self.FillNeighbors(MeSHEdgeInName) 
        sys.setrecursionlimit(10000)   
        pickle.dump(self.hMeSH, open(self.MeSHTermDictIn,'wb'))
        print "generated, dump to [%s]" %(self.MeSHTermDictIn)
        return
    
    def FillNeighbors(self,MeSHEdgeInName):
        '''
        read MeSHEdgeInName,
        get to each obj's neighbors, fetch its MeSHTerm in self.hMeSH, and put in
        '''
        print 'start fill edge for [%d] mesh term' %(len(self.hMeSH))
        Reader = KeyFileReaderC()
        Reader.open(MeSHEdgeInName)
        for lvCol in Reader:
            if [] == lvCol:
                continue
            ID = lvCol[0][0]
            if not ID in self.hMeSH:
                continue
            lNeighbor = []
            for vCol in lvCol:
                if not vCol[2] in self.hMeSH:
                    continue
                DstNode = self.hMeSH[vCol[2]]
                lNeighbor.append([vCol[1],DstNode])
            print '[%s] get [%d] neighbor' %(ID,len(lNeighbor))
            if not 'neighbor' in self.hMeSH[ID].hBase:
                self.hMeSH[ID].hBase['neighbor'] = lNeighbor
            else:
                self.hMeSH[ID].hBase['neighbor'] += lNeighbor         
        
        return    
        
    
    
    
    def SegObjIdFromFName(self,FName):
        return MeSHTermC.SegObjIdFromFName(ntpath.basename(FName))  
    
    def FetchObj(self,ObjId):
        if {} == self.hMeSH:
            print "loading meshtermdict in from [%s]" %(self.MeSHTermDictIn)
            sys.setrecursionlimit(10000)
            self.hMeSH = pickle.load(open(self.MeSHTermDictIn))
        
        MeSHTerm = MeSHTermC()
        MeSHTerm.hBase['id'] = ObjId
        if ObjId in self.hMeSH:
            MeSHTerm = self.hMeSH[ObjId]
            
        return MeSHTerm
   
                
     
