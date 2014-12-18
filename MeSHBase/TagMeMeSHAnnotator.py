'''
Created on Dec 18, 2014 1:36:34 PM
@author: cx

what I do:
I annotate query by tagme, use the spots and linked wiki entity, find whether
it appears in mesh by exact match
what's my input:
query
what's my output:
[[UI,MeSHTerm]]

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
from TagMeAPI.TagMeAPIBase import TagMeAPIBaseC
from MeSHBase.MeSHTermCenter import MeSHTermCenterC
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from cxBase.TextBase import TextBaseC
import json
class TagMeMeSHAnnotatorC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.Tagger = TagMeAPIBaseC()
        self.MeSHMapper = MeSHTermCenterC()
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.MeSHMapper.SetConf(ConfIn)
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        MeSHTermCenterC.ShowConf()
        
        
        
    def AnnotateQuery(self,query):
        print "Annotate MeSH term using TagMe [%s]" %(query)
        
        lhAna = self.Tagger.TagText(query)
        lTermWithUI = []
        for hAna in lhAna:
            Entity = hAna['title'].lower()
            Spot = hAna['spot'].lower()
            lTerm = [Entity]
            if Spot != Entity:
                lTerm.append(Spot)
            for term in lTerm:
                term = term.encode('ascii','ignore')
                UI = self.MeSHMapper.MapTerm(term)
                if UI == "":
                    print "tagged [%s] not found in MeSH" %(term)
                    continue
                lTermWithUI.append([UI,term])
        print "[%s] TagMeSh:\n%s" %(query,json.dumps(lTermWithUI))
        return lTermWithUI
        
    

