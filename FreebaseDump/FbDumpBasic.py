'''
Created on Feb 7, 2014
basic operations on Freebase dump data
@author: cx
'''

TypeEdge = "<http://rdf.freebase.com/ns/type.object.type>"
DespEdge = "<http://rdf.freebase.com/ns/common.topic.description>"
NameEdge = "<http://www.w3.org/2000/01/rdf-schema#label>"
AliasEdge = "<http://rdf.freebase.com/ns/common.topic.alias>"
def GetId(col):
    target = DiscardPrefix(col)
    if len(target) < 2:
        return ""
    if (target[:len('m/')] == "m/") | (target[:len('en/')]=='en/'):
        return target
    return ""

def IsTypeEdge(edge):
    if edge == TypeEdge:
        return True
    return False
def GetType(vCol):
    if IsTypeEdge(vCol[1]):
        Type = DiscardPrefix(vCol[2])
        if Type == "common/topic":
            return ""
        return DiscardPrefix(vCol[2])
    return ""

def DiscardPrefix(col):
    mid = col.strip("<").strip(">")
    vCol = mid.split("/")
    target = vCol[len(vCol)-1]
    return target.replace('.','/')





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
    
def GetDesp(lObj):
    #get desp
    desp = ""
    for vCol in lObj:
        if vCol[1] == DespEdge:
            desp,tag = SegLanguageTag(vCol[2])
    return desp
