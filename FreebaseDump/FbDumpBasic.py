'''
Created on Feb 7, 2014
basic operations on Freebase dump data
@author: cx
'''

TypeEdge = "<http://rdf.freebase.com/ns/type.object.type>"
DespEdge = "<http://rdf.freebase.com/ns/common.topic.description>"
NameEdge = "<http://www.w3.org/2000/01/rdf-schema#label>"
AliasEdge = "<http://rdf.freebase.com/ns/common.topic.alias>"
NotableEdge = "<http://rdf.freebase.com/ns/common.topic.notable_types>"
InstanceEdge = "<http://rdf.freebase.com/ns/type.type.instance>"


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

def GetAlias(vCol):
    if not IsAliasEdge(vCol[1]):
        return ""
    if not IsString(vCol[2]):
        return ""
    alias,en = SegLanguageTag(vCol[2])
    if (en != "") &(en != 'en'):
        alias = ""
    return alias
    
    


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
