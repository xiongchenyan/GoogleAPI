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


import site

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from cxBase.base import cxBaseC,cxConf
from ObjCenter.ObjCacheCenter import ObjCacheCenterC
from MeSHBase.MeSHTerm import MeSHTermC
import ntpath
import pickle
class MeSHObjCacheCenterC(ObjCacheCenterC):
    def Init(self):
        ObjCacheCenterC.Init(self)
        self.hMeSH = {}  #id -> MeSHTerm hBase
        self.MeSHTermDictIn = ""
        
    def SetConf(self, ConfIn):
        ObjCacheCenterC.SetConf(self, ConfIn)
        self.MeSHTermDictIn = self.WorkDir + 'meshtermdict'
        
        
    
    def FormMeSHTermDict(self,RawMeSHInName):
        '''
        generate the MeSHTerm dict
        load each record
            seg to MeSHTermC
            add hBase to hMeSH
        dump
        '''
        
        cnt = 0
        lLine = []
        for line in open(RawMeSHInName):
            line = line.strip()
            if line == '*NEWRECORD':
                MeSHTerm = MeSHTermC()
                MeSHTerm.SegFromRawLines(lLine)
                self.hMeSH[MeSHTerm.GetField('id')] = MeSHTerm.hBase
                cnt += 1
                if 0 == (cnt % 100):
                    print "generating dict, processed [%d] term" %(cnt)
                lLine = []
            lLine.append(line)
        MeSHTerm = MeSHTermC()
        MeSHTerm.SegFromRawLines(lLine)
        self.hMeSH[MeSHTerm.GetField('id')] = MeSHTerm.hBase    
        pickle.dump(self.hMeSH, open(self.MeSHTermDictIn,'wb'))
        print "generated, dump to [%s]" %(self.MeSHTermDictIn)
        return
        
        
    
    
    
    def SegObjIdFromFName(self,FName):
        return MeSHTermC.SegObjIdFromFName(ntpath.basename(FName))  
    
    def FetchObj(self,ObjId):
        if {} == self.hMeSH:
            print "loading meshtermdict in from [%s]" %(self.MeSHTermDictIn)
            self.hMeSH = pickle.load(open(self.MeSHTermDictIn))
        
        MeSHTerm = MeSHTermC()
        MeSHTerm.hBase['id'] = ObjId
        if ObjId in self.hMeSH:
            MeSHTerm = MeSHTermC(self.hMeSH[ObjId])
            
        return MeSHTerm
   
                
     
