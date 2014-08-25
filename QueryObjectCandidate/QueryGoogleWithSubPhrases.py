'''
Created on Aug 25, 2014
for all sub queries, call google search api, and get results.
in: raw query + stemmed query + output
out: qid\tquery\tobj\tscore\tsub query used
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
# site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')
# site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
# site.addsitedir('/bos/usr0/cx/PyCode/ConvexFrameworkQueryExpansion')
import sys
from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
from GoogleFreebaseAPI.APIBase import *
from GoogleFreebaseAPI.SearchAPI import *
from cxBase.TextBase import *

class QueryGoogleWithSubPhrasesC(cxBaseC):
    def Init(self):
        self.InQuery = ""
        self.InStemQuery = "" #used to output
        self.MinPhraseLen = 2
        self.OutName = ""
        self.NumOfObjPerQ = 20
        
    def SetConf(self,ConfIn):
        conf = cxConfC(ConfIn)
        self.InQuery = conf.GetConf('in')
        self.InStemQuery = conf.GetConf('stemmedq',self.InQuery)
        self.MinPhraseLen = int(conf.GetConf('minphraselen',self.MinPhraseLen))
        self.OutName = conf.GetConf('out')
        self.NumOfObjPerQ = int(conf.GetConf('numofobj',self.NumOfObjPerQ))
        
    @staticmethod
    def ShowConf():
        print "in\nstemmedq\nminphraselen\nout\nnumofobj"
        
        
    def LoadStemQ(self):
        self.hStemQ = {}
        for line in open(self.InStemQuery):
            qid,query = line.strip().split('\t')
            self.hStemQ[qid] = query
    
    def FormSubPhrases(self,query):
        lSubPhrase = [query]
        StopQuery = TextBaseC.DiscardStopWord(query)
        vCol = StopQuery.split()
        L = len(vCol)
        while L >= self.MinPhraseLen:
            for i in range(len(vCol) - L + 1):
                lSubPhrase.append(' '.join(vCol[i:i + L]))
            L = L - 1
        return lSubPhrase
    
    
    def FetchObjForPhrase(self,phrase):
        lObj = SearchFreebase(phrase)[:self.NumOfObjPerQ]
        return lObj
    
    def ProcessOneQ(self,qid, query):
        lSubPhrase = self.FormSubPhrases(query)
        #not filtering now, keep everything
        
        lResLine = []
        
        for phrase in lSubPhrase:
            print "searching for [%s]" %(phrase)
            lObj = self.FetchObjForPhrase(phrase)
            for Obj in lObj:
                lResLine.append(qid + '\t' + self.hStemQ[qid]  + '\t' + Obj.GetId().encode('utf-8','ignore') + '\t%f'%(Obj.GetScore()) + '\t' + phrase)
        return lResLine
    
    def Process(self):
        
        self.LoadStemQ()
        
        out = open(self.OutName,'w')
        for line in open(self.InQuery):
            qid,query = line.strip().split('\t')
            print "working on [%s][%s]" %(qid,query)
            lRes = self.ProcessOneQ(qid, query)
            print >> out, '\n'.join(lRes)
        out.close()        
        print "finished"
        
        
import sys
if 2 != len(sys.argv):
    print "conf"
    QueryGoogleWithSubPhrasesC.ShowConf()
    sys.exit()
    
Runner = QueryGoogleWithSubPhrasesC(sys.argv[1])
Runner.Process()        
