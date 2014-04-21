'''
Created on Feb 10, 2014
filter fb dump
    discard other languages
    discard non-utf 8 coding strings
@author: cx
'''

import site
site.addsitedir('/bos/usr4/cx/cxPylib')
import sys
from FbDumpBasic import *
from cxBase.base import cxConf
import gzip

lKeepEdge = [NameEdge,TypeEdge,DespEdge,AliasEdge]
hKeepEdge = dict(zip(lKeepEdge,range(len(lKeepEdge))))

def ContainReqEdge(vCol):
    if vCol[1] in hKeepEdge:
        return True
    return False

def NotANonEngStr(vCol):
    if not IsString(vCol[2]):
        return True
    text,lang = SegLanguageTag(vCol[2])
    if ("" != lang) & ("en" != lang):
        return False
    return True

def DesIsObj(vCol):
    ObjId = GetId(vCol[2])
    if "" != ObjId:
        return True
    return False


if 2 != len(sys.argv):
    print "1 para: conf \nin\nout"
    sys.exit()

conf = cxConf(sys.argv[1])
InName = conf.GetConf('in')
OutName = conf.GetConf('out')

    
out = gzip.open(OutName,'w')
cnt = 0
outcnt = 0
for line in gzip.open(InName):
    cnt += 1
    if 0 == (cnt % 10000):
        print "processed [%d] keep [%d]" %(cnt,outcnt)
    line = line.strip()
    vCol = line.split('\t')
    if NotANonEngStr(vCol):        
        try:
            print >> out, line
            outcnt += 1
        except UnicodeDecodeError:
            continue    
    
out.close()
print "left [%d] line in [%d]" %(outcnt,cnt)
