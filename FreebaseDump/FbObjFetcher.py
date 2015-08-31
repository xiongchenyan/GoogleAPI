'''
Created on Aug 31, 2015 11:42:06 AM
@author: cx

what I do:
    I fetch fb obj from dump
    with given Freebase obj id, or Wiki en_id
        if startswith('/m/') then Fb Id
        else: wiki id
what's my input:
    Fb dump (rdf in gz)
    Fb id list, or Wiki id list
what's my output:
    the FbObj, with attributes/neighbors filled
    dumpped to given dir, in given format

'''


import site

site.addsitedir("/bos/usr0/cx/PyCode/cxPyLib")
site.addsitedir("/bos/usr0/cx/PyCode/GoogleAPI")

from ObjCenter.FbObjCacheCenter import FbObjCacheCenterC
from ObjCenter.FbObjBase import FbObjC
from FbDumpReader import FbDumpReaderC
from FbDumpBasic import FbDumpOpeC

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
import logging
import pickle

class FbObjFetcherC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.DumpInName = ""
        self.sTargetObjId = {}
        self.TargetIdInName = ""
        self.ObjCenter = FbObjCacheCenterC()
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.DumpInName = self.conf.GetConf('fbdumpin')
        self.TargetIdInName = self.conf.GetConf('targetidin')
        self.sTargetObjId = set(open(self.TargetIdInName).read().splitlines())
        logging.info('[%d] target obj',len(self.sTargetObjId))
        self.ObjCenter.SetConf(ConfIn)
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'fbdumpin\ntargetidin'
        FbObjCacheCenterC.ShowConf()
        
        
    def Process(self):
        
        reader = FbDumpReaderC()
        reader.open(self.DumpInName)
        cnt = 0
        FindCnt = 0
        hWikiIdObjInfo = {}
        for lvCol in reader:
            FbObj = FbObjC()
            FbObj.FormFromDumpData(lvCol)
            
            if (FbObj.GetId() in self.sTargetObjId) | (FbObj.GetWikiId() in self.sTargetObjId):
                self.ObjCenter.DumpObj(FbObj)
                logging.info('dumpped obj [%s][%s]',FbObj.GetId(),FbObj.GetName())
                FindCnt += 1
            if FbObj.GetWikiId() in self.sTargetObjId:
                hWikiIdObjInfo[FbObj.GetWikiId()] = [FbObj.GetId(),FbObj.GetName()]
                
                
            cnt += 1
            if 0 == (cnt % 10000):
                logging.info('processed [%d] obj, dumped [%d]',cnt,FindCnt)
        
        self.WriteWikiObjInfo(hWikiIdObjInfo)                
        logging.info('finished [%d/%d] find',FindCnt,len(self.sTargetObjId))
        return True
    
    def WriteWikiObjInfo(self,hWikiIdObjInfo):
        out = open(self.ObjCenter.WorkDir + '/WikiIdObjInfo','a')
        for key,item in hWikiIdObjInfo.items():
            print >>out, key + '\t' + '\t'.join(item)
            
        out.close()
        logging.info('wiki obj infor added to %s/WikiIdObjInfo',self.ObjCenter.WorkDir )
        return
            
            
        
        
    
if __name__ == '__main__':
    import sys
    if 2 != len(sys.argv):
        print 'I fetch given obj id/wiki id from fb dump'
        FbObjFetcherC.ShowConf()
        sys.exit()
        
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
#     ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)       

        
    Processor = FbObjFetcherC(sys.argv[1])
    Processor.Process()        
        
        
        
    

