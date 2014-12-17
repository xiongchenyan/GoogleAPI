'''
Created on Dec 17, 2014 5:10:50 PM
@author: cx

what I do:
I map term to MeSH UI (Uniq id)

include:
    make the dict
    do exact match from term|alias -> UI
what's my input:
term -> UI
and make dict    
what's my output:


'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
import pickle

from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from cxBase.TextBase import TextBaseC

class MeSHTermCenterC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.DictDumpPath = ""
        self.hTermUI = {}   #term -> UI
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.DictDumpPath = self.conf.GetConf('meshtermdict')


    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print "meshtermdict"
            
    def FormDictFromRawMeSH(self,InName):
        
        lLine = []
        for line in open(InName):
            line = line.strip()
            if "*NEWRECORD" == line:
                hThisTerm = self.SegNameAliasAndUIFromRawMeSH(lLine)
                self.hTermUI.update(hThisTerm)
                lLine = []
            lLine.append(line)
        pickle.dump(self.hTermUI,open(self.DictDumpPath,'wb'))
        print "dict dump to [%s]" %(self.DictDumpPath)
        return
    
    def SegNameAliasAndUIFromRawMeSH(self,lLines):
        lTerm = []
        UI = ""
        for line in lLines:
            vCol = line.split('=')
            head = vCol[0].strip(' ')
            content = ' '.join(vCol[1:]).strip(' ')
            if head == 'MH':
                lTerm.append(content.lower())
            if (head == 'ENTRY') | (head == 'PRINT ENTRY'):
                term = content.split('|')[0]
                term = TextBaseC.RawClean(term)
                lTerm.append(term)
            if (head == 'UI'):
                UI = content
        hDict = dict(zip(lTerm,[UI] * len(lTerm)))
        return hDict
    
    def MapTerm(self,term):
        if self.hTermUI == {}:
            if "" != self.DictDumpPath:
                print "read dict from [%s]" %(self.DictDumpPath)
                self.hTermUI = pickle.load(open(self.DictDumpPath))
        term = term.lower()
        if term in self.hTermUI:
            return self.hTermUI[term]
        return ""