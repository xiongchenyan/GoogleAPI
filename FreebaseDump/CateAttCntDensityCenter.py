'''
Created on May 27, 2014
estimate the density of category in dump
input: per object category att cnt, each line is cate\ncnt
output: a cate gory density cnt for each category
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')

from DensityEstimation.EmpiricalCDF import *
from cxBase.base import cxBaseC,cxConf

class CateAttCntDensityCenterC(cxBaseC):
    def Init(self):
        self.hCateDensity = {}
        
        
    def MakeFromCnt(self,CntInName):
        #may out of mem, be aware (oom at cluster, not head)
        hCateCnt = {}
        
        for line in open(CntInName):
            name,cnt = line.strip().split('\t')
            if not name in hCateCnt:
                hCateCnt[name] = [int(cnt)]
            else:
                hCateCnt[name].append(int(cnt))
        
        for item in hCateCnt:
            CDF = EmpiricalCDFC()
            CDF.Make(hCateCnt[item])
            self.hCateDensity[item] = CDF 
        return True
    
    def dump(self,OutName):
        out = open(OutName,'w')
        for item in self.hCateDensity:
            print >>out, item + "\t" + self.hCateDensity[item].dumps()
        out.close()
        return True
    
    def load(self,InName):
        for line in open(InName):
            vCol = line.strip().split('\t')
            name = vCol[0]
            CDF = EmpiricalCDFC()
            CDF.loads('\t'.join(vCol[1:]))
            self.hCateDensity[name] = CDF
        return True
    
    
    def empty(self):
        return {} == self.hCateDensity
    
    def clear(self):
        self.hCateDensity.clear()
        
    def GetProb(self,cate,cnt):
        if not cate in self.hCateDensity:
            return 0
        return self.hCateDensity[cate].GetCdf(cnt)
    
    