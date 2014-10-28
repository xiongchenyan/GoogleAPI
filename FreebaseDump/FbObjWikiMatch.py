'''
Created on Oct 27, 2014 7:10:39 PM
@author: cx

what I do:
match objid in Freebase with Wikipedia
match is done by the Wiki Url field of Obj
function supported:
generate obj-wiki match dump:
    input:
        FbDump
    output:
        pickle dump of dicts obj->wiki and wiki->obj
Match obj and wiki
    input: pickle dump name
    do: objid -> wiki url
        wiki url -> objid
'''



import site
site.addsitedir("/bos/usr0/cx/PyCode/cxPyLib")
site.addsitedir("/bos/usr0/cx/PyCode/GoogleAPI")

from FreebaseDump.FbDumpReader import FbDumpReaderC
from FreebaseDump.FbDumpBasic import FbDumpOpeC

from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import pickle

class FbObjWikiMatchC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.FbDumpName = ""
        self.DictDumpName = ""
        self.hObjWiki = {}
        self.hWikiObj = {}
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.FbDumpName = self.conf.GetConf('fbdump')
        self.DictDumpName = self.conf.GetConf('fbwikidump')
        
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'fbdump\nfbwikidump'
        
        
    def GenerateDictDump(self):
        hObjWiki = {}
        hWikiObj = {}
        
        Reader = FbDumpReaderC()
        Reader.open(self.FbDumpName)
        Ope = FbDumpOpeC()
        cnt = 0
        ObjCnt = 0;
        for lvCol in Reader:
            ObjId = Ope.GetObjId(lvCol)
            lWikiUrl = Ope.GetWikiUrl(lvCol)
            ObjCnt += 1
            if 0 == (ObjCnt % 10000):
                print "read [%d] raw obj" %(ObjCnt)
            if  ('' == ObjId):
                continue
            if ([] == lWikiUrl):
                print "[%s][%s] has no wiki url" %(ObjId,'\n'.join(Ope.GetName(lvCol)))
                continue
            hObjWiki[ObjId] = lWikiUrl
            cnt += 1
            for WikiUrl in lWikiUrl:
                if not WikiUrl in hWikiObj:
                    hWikiObj[WikiUrl] = [ObjId]
                else:
                    hWikiObj[WikiUrl].append(ObjId)
        
            if 0 == (cnt % 1000):
                print 'processed [%d] obj with wikiurl' %(cnt)
        print 'dict generated size [%d][%d]' %(len(hObjWiki),len(hWikiObj))
        out = open(self.DictDumpName,'wb')
        pickle.dump([hObjWiki,hWikiObj],out)
        out.close()
        print "dump finished"    
        
        
    def MatchWikiToObj(self,WikiUrl):
        if {} == self.hWikiObj:
            In = open(self.DictDumpName)
            self.hObjWiki,self.hWikiObj = pickle.load(In)
            print 'load dict dump done'
        if WikiUrl in self.hWikiObj:
            return self.hWikiObj[WikiUrl]
        else:
            return []
        
    def MatchObjToWiki(self,ObjId):
        if {} == self.hWikiObj:
            In = open(self.DictDumpName)
            self.hObjWiki,self.hWikiObj = pickle.load(In)
            print 'load dict dump done'
        if ObjId in self.hObjWiki:
            return self.hObjWiki[ObjId]
        else:
            return []
            
    
    
    
    
        
