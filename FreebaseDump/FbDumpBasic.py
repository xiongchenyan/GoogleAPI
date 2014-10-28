'''
Created on Feb 7, 2014
basic operations on Freebase dump data
@author: cx
'''

'''
Oct 27, 2014
Added get multiple alias func
Added get wiki url func
and reconstructed them as a class
'''

TypeEdge = "<http://rdf.freebase.com/ns/type.object.type>"
DespEdge = "<http://rdf.freebase.com/ns/common.topic.description>"
NameEdge = "<http://www.w3.org/2000/01/rdf-schema#label>"
AliasEdge = "<http://rdf.freebase.com/ns/common.topic.alias>"
NotableEdge = "<http://rdf.freebase.com/ns/common.topic.notable_types>"
InstanceEdge = "<http://rdf.freebase.com/ns/type.type.instance>"
WikiUrlEdge = "<http://rdf.freebase.com/ns/common.topic.topic_equivalent_webpage>"

import json

class FbDumpOpeC(object):
    def __init__(self):
        self.TypeEdge = "<http://rdf.freebase.com/ns/type.object.type>"
        self.DespEdge = "<http://rdf.freebase.com/ns/common.topic.description>"
        self.NameEdge = "<http://www.w3.org/2000/01/rdf-schema#label>"
        self.AliasEdge = "<http://rdf.freebase.com/ns/common.topic.alias>"
        self.NotableEdge = "<http://rdf.freebase.com/ns/common.topic.notable_types>"
        self.InstanceEdge = "<http://rdf.freebase.com/ns/type.type.instance>"
        self.lWikiUrlEdge = ["<http://rdf.freebase.com/ns/common.topic.topic_equivalent_webpage>","<http://rdf.freebase.com/ns/common.topic.topical_webpage>"]
        
    @staticmethod
    def GetObjId(lvCol):
        if lvCol == []:
            return ""
        return FbDumpOpeC.GetId(lvCol[0][0])        
    
    @staticmethod
    def DiscardPrefix(col):
        if len(col) < 2:
            return col
        if (col[0] != '<') | (col[len(col) - 1] !=">"):
            return col    
        mid = col.strip("<").strip(">")
        vCol = mid.split("/")
        target = vCol[len(vCol)-1]
        return '/' + target.replace('.','/')
    
    @staticmethod
    def GetId(col):
        target = FbDumpOpeC.DiscardPrefix(col)
        if len(target) < 2:
            return ""
        if (target[:len('/m/')] == "/m/") | (target[:len('/en/')]=='/en/'):
            return target
        return ""
    
    @staticmethod
    def FetchTargetsWithEdge(lvCol,Edge):
        '''
        fetch col with edge (obj edge col)
        '''
        lTar = []
        for vCol in lvCol:
            if vCol[1] == Edge:
                lTar.append(vCol[2])

        return lTar
    
    @staticmethod
    def FetchTargetStringWithEdge(lvCol,Edge):
        '''
        same, but only look for english strings
        '''
        lTar = FbDumpOpeC.FetchTargetsWithEdge(lvCol, Edge)        
#         print 'curent obj:%s' %(json.dumps(lvCol))
#         print 'edge [%s] get targets [%s]' %(Edge,json.dumps(lTar))
        lStr = []
        for tar in lTar:
            if not FbDumpOpeC.IsString(tar):
                continue
            text,tag = FbDumpOpeC.SegLanguageTag(tar)
            if (tag == "") | (tag == 'en'):
                lStr.append(text)
#         print 'get text [%s]' %(json.dumps(lStr))
        return lStr
    
    
    
    
    def GetName(self,lvCol):
        lStr = self.FetchTargetStringWithEdge(lvCol, self.NameEdge)
        return lStr
    
    def GetAlias(self,lvCol):
        return self.FetchTargetStringWithEdge(lvCol, self.AliasEdge)
    
    def GetDesp(self,lvCol):
        return '\n'.join(self.FetchTargetStringWithEdge(lvCol, self.DespEdge))
    
    def GetWikiUrl(self,lvCol):
        lWikiUrl = []
        for edge in self.lWikiUrlEdge:
            lTar = self.FetchTargetsWithEdge(lvCol, edge)
#             if [] != lTar:
#                 print 'wiki target %s' %(json.dumps(lTar))
            
            for tar in lTar:
                if not 'http' in tar:
                    continue
                if not 'en.wikipedia' in tar:
                    continue
                lWikiUrl.append(tar.strip('<').strip('>'))
#         if [] != lWikiUrl:
#             print 'wikiurl: %s' %(json.dumps(lWikiUrl))
        return lWikiUrl
    
    def GetType(self,lvCol):
        lTar = self.FetchTargetsWithEdge(lvCol, self.TypeEdge)
        lType = []
        for tar in lTar:
            Type = self.DiscardPrefix(tar)
            if '/common' == Type[:len('/common')]:
                continue          
            lType.append(Type)
        return lType
    
    def GetNotable(self,lvCol):
        lTar = self.FetchTargetsWithEdge(lvCol, self.NotableEdge)
        return [self.DiscardPrefix(item) for item in lTar]
        
    
    
            
        
    @staticmethod
    def IsString(s):
        if s[0] != '\"':
            return False
        if s[-1] == '\"':
            return True
        vCol = s.split('@')
        if vCol[0][-1] == '\"':
            return True
        return False
    
    @staticmethod     
    def SegLanguageTag(s):
        vCol = s.split("@")
        if (len(vCol) < 2):
            return s,""
        else:
            return vCol[0],vCol[1]
    
    
    

def GetId(col):
    target = DiscardPrefix(col)
    if len(target) < 2:
        return ""
    if (target[:len('/m/')] == "/m/") | (target[:len('/en/')]=='/en/'):
        return target
    return ""

def IsId(col):
    if "" != GetId(col):
        return IsId

def IsTypeEdge(edge):
    return DiscardPrefix(edge) == DiscardPrefix(TypeEdge)

def GetType(vCol):
    if IsTypeEdge(vCol[1]):
        Type = DiscardPrefix(vCol[2])
        if Type == "/common/topic":
            return ""
        return DiscardPrefix(vCol[2])
    return ""

def IsNameEdge(edge):
    return DiscardPrefix(edge) == DiscardPrefix(NameEdge)

def GetName(lvCol):
    name = ""
    for vCol in lvCol:
        if IsNameEdge(vCol[1]):
            if not IsString(vCol[2]):
                continue
            name,en = SegLanguageTag(vCol[2])
            if (en != "") &(en != 'en'):
                name = ""
    return name

def IsAliasEdge(edge):
    return DiscardPrefix(edge) == DiscardPrefix(AliasEdge)

def GetAlias(lvCol):
    if type(lvCol) != list:
        lvCol = [lvCol]
    lAlias = []
    for vCol in lvCol:
        if not IsAliasEdge(vCol[1]):
            continue
        if not IsString(vCol[2]):
            continue
        alias,en = SegLanguageTag(vCol[2])
        if (en != "") &(en != 'en'):
            continue
        lAlias.append(alias)
    return lAlias
    
    


def DiscardPrefix(col):
    if len(col) < 2:
        return col
    if (col[0] != '<') | (col[len(col) - 1] !=">"):
        return col    
    mid = col.strip("<").strip(">")
    vCol = mid.split("/")
    target = vCol[len(vCol)-1]
    return '/' + target.replace('.','/')




def IsInstanceEdge(edge):
    return DiscardPrefix(edge) == DiscardPrefix(InstanceEdge)


def GetDomain(col):
    raw = DiscardPrefix(col).strip('/')
    vCol = raw.split('/')
    
    if vCol[0] != 'cotype':    
        return vCol[0]
    return 'cotype' + vCol[1]

def GetNotableType(lObj):
    if type(lObj) == list:
        lvCol = lObj
    else:
        lvCol = [line.split('\t') for line in lObj]
        
    for vCol in lvCol:
        if (vCol[1] == NotableEdge) | (vCol[1] == DiscardPrefix(NotableEdge)):
            return DiscardPrefix(vCol[2])
    return "" 
        
    


def IsString(s):
    if s[0] != '\"':
        return False
    if s[len(s) - 1] == '\"':
        return True
    vCol = s.split('@')
    if vCol[0][len(vCol[0])-1] == '\"':
        return True
    return False
    
         
def SegLanguageTag(s):
    vCol = s.split("@")
    if (len(vCol) < 2):
        return s,""
    else:
        return vCol[0],vCol[1]
    
def GetDesp(lvCol):
    #get desp
    desp = ""
    for vCol in lvCol:
        if (vCol[1] == DespEdge) | (vCol[1] == DiscardPrefix(DespEdge)):
            desp,tag = SegLanguageTag(vCol[2])
            if (tag != "") & (tag != "en"):
                desp = ""
    return desp
