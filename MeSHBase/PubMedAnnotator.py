'''
Created on Dec 17, 2014 7:09:39 PM
@author: cx

what I do:
I annotate query by issuing it to PubMed
what's my input:
textual query
what's my output:
annotated MeSh terms and UI
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from cxBase.TextBase import TextBaseC
from MeSHBase.MeSHTermCenter import MeSHTermCenterC
import urllib
import time
import json
class PubMedAnnotatorC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.MeSHTermCenter = MeSHTermCenterC()
        self.PubMedUrl = "http://www.ncbi.nlm.nih.gov/pubmed/?term="
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.MeSHTermCenter.SetConf(ConfIn)
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        MeSHTermCenterC.ShowConf()
        
    
    
    def AnnotateQuery(self,query):
        url = self.PubMedUrl + query
        data = self.FetchUrlData(url)
        RawAnaQuery = self.SegPubMedReturnPage(data)
        lTerm = self.SegTermFromRawAna(RawAnaQuery)
        print "q [%s] RawANA [%s] term %s" %(query,RawAnaQuery,json.dumps(lTerm))
        
        lTermWithUI = []
        for term in lTerm:
            UI = self.MeSHTermCenter.MapTerm(term)
            if "" == UI:
                print "term [%s] not matched to UI" %(term)
                continue
            lTermWithUI.append([UI,term])
        return lTermWithUI
        
        
    def FetchUrlData(self,url):
        cnt = 0
        data = ""
        while (cnt < 10):
            try:
                data = urllib.urlopen(url).read()
            except IOError:
                time.sleep(1)
                print "IOError, wait [%d] time" %(cnt)
                cnt += 1
                continue
            break    
        return data

    def SegPubMedReturnPage(self,data):
        #looking for searchdetails_term, then get those in between ("pubmed">) (</textarea>)
        st = data.index('searchdetails_term')
        RawQSt = data[st:].index("pubmed\">") + st + len('pubmed\">')
        RawQEd = data[RawQSt:].indeX("</textarea>") + RawQSt
        RawQ = data[RawQSt:RawQEd]
        
        return RawQ

    def SegTermFromRawAna(self,RawAnaQuery):
        '''
        parse the q by space out of "" and []
        get those with suffix "[MeSH Terms]"
        '''
        lTerm = []
        
        ToParseQ = ""
        MarkCnt = 0
        BraceFlag = 0
        for c in RawAnaQuery:
            if c == "\"":
                MarkCnt += 1
            if c == '[':
                BraceFlag += 1
            if c == ']':
                BraceFlag -= 1
            if c == ' ':
                if (BraceFlag == 0) & ((MarkCnt % 2)==0):
                    c = '\t'
            ToParseQ += c
        lTermWithAna = ToParseQ.split('\t')
        for TermAna in lTermWithAna:
            if "[MeSH Terms]" == TermAna[-12:]:
                lTerm.append(TermAna[:-12].strip('\"'))
        return lTerm
            
        
        
        
        