'''
Created on Feb 16, 2015 4:09:25 PM
@author: cx

what I do:
I extract edge from mesh
there are two types of edges:
    belong to (defined by tree no)
    annotated to (defined by CAPITAL letter in description)
So there are four edges, as the two types are directional:
    IsSubClass
    IsSuperClass
    AnnotatedTo
    Contain
what's my input:
MeSH Raw Data
what's my output:
MeSHId\tedge type\t MeSH Id: a->b

'''


import site
site.addsitedir("/bos/usr0/cx/PyCode/cxPyLib")
site.addsitedir("/bos/usr0/cx/PyCode/GoogleAPI")
import json
import sys,pickle
from cxBase.Conf import cxConfC
from cxBase.SeparatorlineFileReader import SeparatorlineFileReaderC

def FormTreeNoMapping(InName):
    hTreeNoMeSH = {}   #treeno (MN)->MeSHId (UI)
    Reader = SeparatorlineFileReaderC()
    Reader.Spliter = '='
    Reader.SeparatorPre = '*NEWRECORD'
    Reader.open(InName)
    
    for lvCol in Reader:
        lItem = [vCol[:2] for vCol in lvCol if len(vCol) > 1]
        hItem = dict(lItem)
        if (not 'UI' in hItem) | (not 'MN' in hItem):
            continue
        ID = hItem['UI']
        TreeNO = hItem['MN']
                
        hTreeNoMeSH[TreeNO] = ID        
    Reader.close()    
    return hTreeNoMeSH




def GenerateEdge(InName,OutName, hTreeNoMeSH,hTermID):
    Reader = SeparatorlineFileReaderC()
    Reader.Spliter = '='
    Reader.SeparatorPre = '*NEWRECORD'
    
    out = open(OutName,'w')
    Reader.open(InName)
    for lvCol in Reader:
        lTriple = ProcessOneMeSH(lvCol, hTreeNoMeSH, hTermID)
        for triple in lTriple:
            print >>out,'\t'.join(triple)
        
    out.close()
    Reader.close()
    
    
    return

def FatherTreeNO(TreeNo):
    FatherNo = '.'.join(TreeNo.split('.')[:-1])
    if FatherNo == TreeNo:
        return ""
    return FatherNo

def ProcessOneMeSH(lvCol,hTreeNoMeSH,hTermID):
    lTriple = []
    hItem = dict([vCol[:2] for vCol in lvCol if len(vCol) > 1])

    try:
        desp  = hItem['MS']
        ID = hItem['UI']
        TreeNo = hItem['MN']
    except KeyError:
        return []
    
    FatherNo =FatherTreeNO(TreeNo)
    if (FatherNo != '') & (FatherNo in hTreeNoMeSH):
        FatherId = hTreeNoMeSH[FatherNo]
        lTriple.append([ID,'IsSub',FatherId])
        lTriple.append([FatherId,'IsSuper',ID])
        
        
    print 'ID[%s] desp [%s]' %(ID,desp)
    for term in desp.split():
        if term.isupper():
            term = term.lower()
            if term in hTermID:
                AnaId = hTermID[term]
                lTriple.append([ID,'Contain',AnaId])
                lTriple.append([AnaId,'AnaTo',ID])
            else:
                print term + ' not in term id dict'
    
    return lTriple
    
    
    


if 2 != len(sys.argv):
    print 'conf\nin\nout\ntermdictin\n'
    sys.exit()
    
conf = cxConfC(sys.argv[1])
InName = conf.GetConf('in')
OutName = conf.GetConf('out')
TermDictIn = conf.GetConf('termdictin')
hTermID = pickle.load(open(TermDictIn))

hTreeNoMeSH = FormTreeNoMapping(InName)
print 'tree no mapping made'
GenerateEdge(InName, OutName, hTreeNoMeSH, hTermID)
print 'finished'    



