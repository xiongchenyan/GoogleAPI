'''
Created on May 22, 2014
input: a list of category, one line per file + fb dump
output:     a file, the first n description for them
@author: cx
'''



import site
site.addsitedir("/bos/usr0/cx/PyCode/cxPyLib")
site.addsitedir("/bos/usr0/cx/PyCode/GoogleAPI")

from FreebaseDump.FbDumpReader import *
from FreebaseDump.FbDumpBasic import *
import json
DespPerType = 10000

def LoadTargetCate(InName):
    hType = {}
    global DespPerType
    for line in open(InName):
        hType[line.strip()] = DespPerType
    print "read targets \n%s" %(json.dumps(hType,indent=1))
    return hType


def IsTargetType(domain, hType):
#     print "checking type [%s]" %(domain)
    if not domain in hType:
        print "not in"
        return False
    hType[domain] -= 1
    print "[%s] in, left [%d]" %(domain, hType[domain])
    if hType[domain] == 0:
        del hType[domain]
    return True


def ProcessPerObj(lvCol,hType):
    if not IsId(lvCol[0][0]):
        return []
    Desp = GetDesp(lvCol)

    if "" == Desp:
#         print "[%s] not desp" %(lvCol[0][0])
        return []
#     print "get desp [%s] for [%s]" %(Desp,lvCol[0][0])
#     TypeStr = GetNotableType(lvCol)
    lRes = []
    for vCol in lvCol:
        TypeStr = GetType(vCol)
        if "" != TypeStr:
            if IsTargetType(TypeStr,hType):
                lRes.append([TypeStr,Desp])
    return lRes


import sys


if 5 != len(sys.argv):
    print "4 para: target type + fb dump + out name + number of desp per type"
    sys.exit()
    
InName = sys.argv[1]
FbIn = sys.argv[2]
OutName = sys.argv[3]
DespPerType = int(sys.argv[4])


hType = LoadTargetCate(InName)

FbReader = FbDumpReaderC()
FbReader.open(FbIn)

ObjCnt = 0
cnt = 0
out = open(OutName,'w')
for lvCol in FbReader:
    ObjCnt += 1
    if 0 == (ObjCnt % 1000):
        print "read [%d] obj" %(ObjCnt)
    if len(hType) == 0:
        break
    lRes = ProcessPerObj(lvCol,hType)
    if [] == lRes:
        continue
    cnt += 1
    if 0 == (cnt % 10):
        print "get [%d] desp" %(cnt)
    try:
        for TypeStr,Desp in lRes:     
            print >> out,TypeStr + "\t" + Desp.strip('"')
    except UnicodeDecodeError:
        print "a unicode decode error, discard this desp"
        
out.close()
    
    
