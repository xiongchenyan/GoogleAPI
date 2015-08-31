'''
Created on Aug 31, 2015 11:44:15 AM
@author: cx

what I do:
    I am a new class FbObjC
    I support same API as APIBase.FbApiObjectC
        including: get fields, dumps, and loads
    APIs that no longer needed will not be implemented in this class
    I can be initialized by a group of lines read by FbDumpReaderC
        using functions in FbDumpOpeC
What's my input:
       
what's my output:
    I am a data structure

'''

import json,pickle
from FreebaseDump.FbDumpBasic import FbDumpOpeC
import logging


class FbObjC(object):
    
    def __init__(self):
        self.Init()
        
        
    def Init(self):
        self.lSupportedField = ['name','notabletype','alias','type','Neighbor','desp','id','score']
        self.hData = zip(self.lSupportedField,[None] * len(self.lSupportedField))
        self.FbDumpParser = FbDumpOpeC()
        
    def FormFromDumpData(self,lvCol):
        
        self.hData['id'] = self.FbDumpParser.GetObjId(lvCol)
        self.hData['name'] = self.FbDumpParser.GetName(self, lvCol)
        self.hData['desp'] = self.FbDumpParser.GetDesp(lvCol)
        self.hData['NotableType'] = self.FbDumpParser.GetNotable(lvCol)
        self.hData['alias'] = self.FbDumpParser.GetAlias(lvCol)
        self.hData['neighbor'] = self.FbDumpParser.GetNeighbor(lvCol)
        self.hData['type'] = self.FbDumpParser.GetType(lvCol)
        self.hData['score'] = 0
        
        return True
    
    def GetField(self,field):
        '''
        The unique api to support field name -> results
        field supported:
            name, alias, desp, notabletype,type,neighbor
        please note that the result types differ
        '''
        field = field.lower()
        
        if not field in self.hData:
            logging.error('[%s] not support for obj field',field)
            raise NotImplementedError
        return self.hData[field]
    
    
    def GetId(self):
        return self.GetField('id')
    
    def GetName(self):
        return self.GetField('name')
    
    def GetDesp(self):
        return self.GetField('desp')
    
    def GetAlias(self):
        return self.GetField('alias')
    
    def GetNeighbor(self):
        return self.GetField('neighbor')
    
    def GetNotable(self):
        return self.GetField('notabletype')
    
    def GetScore(self):
        return self.GetField('score')
    
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
            logging.error('dump obj [%s] file can not open', FName)
            raise IOError
            
        pickle.dump(self.hData,out)
        out.close()
        return True
    
    def load(self,InDir):
        FName = InDir + "/" + self.GenerateFName()
        try:
            self.hData = pickle.load(open(FName,'r'))
        except Exception:
            logging.error('load obj [%s] file open failed, please make sure this obj has been prepared\n', FName)
            raise Exception
        return True
