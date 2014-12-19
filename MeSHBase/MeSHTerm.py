'''
Created on Dec 19, 2014 4:46:14 PM
@author: cx

what I do:
I am the base class for MeSHTerm
what's my input:

what's my output:


'''

from copy import deepcopy
import sys,pickle


class MeSHTermC(object):
    def __init__(self,hBase = {}):
        self.Init()
        self.hBase = dict(hBase)
        
    def Init(self):
        self.hBase = {}
        self.MaxFileNameLen = 50
        
    def GetField(self,field):
        '''
        return corresponding field
        '''
        res = ""
        if field == 'alias':
            res = []
        if field == 'type':
            res = []
            
        if field in self.hBase:
            res = self.hBase[field]
            
        return res
    def __deepcopy__(self,memo):
        APIObj = MeSHTermC()
        APIObj.hBase = deepcopy(self.hBase,memo)
        return APIObj
    
    def SegFromRawLines(self,lLine):
        '''
        seg from raw MeSH ASCII lines
        '''
        
        for line in lLine:
            if not '=' in line:
                continue
            vCol = line.split('=')
            head = vCol[0].strip(' ')
            content = ' '.join(vCol[1:]).strip(' ')
            head = head.strip(' ')
            content = content.strip(' ')
            if head == 'MH':
                self.hBase['name'] = content
            if head == 'MS':
                self.hBase['desp'] = content
            if head == 'ENTRY':
                self.lField.append(['alias',content])
                if not 'alias' in self.hBase:
                    self.hBase['alias'] = [content]
                else:
                    self.hBase['alias'].append(content)
            if head == 'UI':
                self.hBase['id'] = content
        return True
    
    
    
    def GenerateFName(self):
        return self.GetField('id')[:self.MaxFileNameLen]
    
    
    
    @staticmethod
    def SegObjIdFromFName(FName):
        return FName
    
    
    def dump(self,OutDir):
        FName = OutDir + "/" + self.GenerateFName()
        try:
            out = open(FName,'w')
        except IOError:
            sys.stderr.write('dump obj [%s] file open failed' %(FName))
            return False
        pickle.dump(self.hBase,out)
        out.close()
        return True
    
    def load(self,InDir):
        FName = InDir + "/" + self.GenerateFName()
        try:
            In = open(FName,'r')
            self.hBase = pickle.load(In)
            In.close()
        except (IOError,EOFError):
            sys.stderr.write('load obj [%s] file open failed\n' %(FName))
            return False
        return True    
    
    
    