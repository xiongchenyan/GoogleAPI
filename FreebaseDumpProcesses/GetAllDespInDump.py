'''
Created on Mar 8, 2015 2:13:57 PM
@author: cx

what I do:
I go through the dump
and output:
name \t mid \t desp
what's my input:
fb dump
what's my output:
name \t mid \t desp

'''


import site
site.addsitedir("/bos/usr0/cx/PyCode/cxPyLib")
site.addsitedir("/bos/usr0/cx/PyCode/GoogleAPI")

from FreebaseDump.FbDumpReader import *
from FreebaseDump.FbDumpBasic import *
import json
DespPerType = 10000






def ProcessPerObj(lvCol):
    if not IsId(lvCol[0][0]):
        return []
    Desp = GetDesp(lvCol)
    
    Name = GetName(lvCol)
    Mid = GetId(lvCol[0][0])
    
    if Mid == '/m/09c7w0':
        print '[%s] dump lines\n%s' %(Mid,json.dumps(lvCol))
    
    if "" == Desp:
#         print "[%s] not desp" %(lvCol[0][0])
        return []
#     print "get desp [%s] for [%s]" %(Desp,lvCol[0][0])
#     TypeStr = GetNotableType(lvCol)

    
    return Name,Mid,Desp
    
    


import sys


if 3 != len(sys.argv):
    print "fb dump + out name"
    sys.exit()
    
FbIn = sys.argv[1]
OutName = sys.argv[2]


FbReader = FbDumpReaderC()
FbReader.open(FbIn)

ObjCnt = 0
cnt = 0
out = open(OutName,'w')
for lvCol in FbReader:
    ObjCnt += 1
    if 0 == (ObjCnt % 1000):
        print "read [%d] obj" %(ObjCnt)
    lRes = ProcessPerObj(lvCol)
    if [] == lRes:
        continue
    cnt += 1
    if 0 == (cnt % 10):
        print "get [%d] desp" %(cnt)
    try:
        Name,Mid,Desp  = lRes     
        print >> out,Name + "\t" + Mid + '\t' + Desp.strip('"')
    except UnicodeDecodeError:
        print "a unicode decode error, discard this desp"
        
out.close()
    
    

