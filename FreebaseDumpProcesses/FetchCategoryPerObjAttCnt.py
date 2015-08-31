'''
Created on May 23, 2014
get the number of attribute in each category for each obj
input: fb dump
output: category \t att count
will be used to estimate the category's attribute probability distribution
    I believe this is an important factor for Google to decide notable_type
@author: cx
'''

import site
site.addsitedir("/bos/usr0/cx/PyCode/cxPyLib")
site.addsitedir("/bos/usr0/cx/PyCode/GoogleAPI")

from FreebaseDump.FbDumpReader import *
from FreebaseDump.FbDumpBasic import *
import json



def SeparateCategory(edge):
    vCol = edge.strip('/').split('/')
    if len(vCol) < 2:
        return ""
    return '/'+ vCol[0] + '/' + vCol[1]


def ProcessOneObj(lvCol):
    hDomainCnt = {}
    for vCol in lvCol:
        edge = vCol[1]
        cate = SeparateCategory(edge)
        if "" == cate:
            continue
        if not cate in hDomainCnt:
            hDomainCnt[cate] = 1
        else:
            hDomainCnt[cate] += 1
    return hDomainCnt


import sys

if 3 != len(sys.argv):
    print "2 para: dump + out"
    sys.exit()
    
FbReader = FbDumpReaderC()
FbReader.open(sys.argv[1])
out = open(sys.argv[2],'w')



cnt = 0
for lvCol in FbReader:
    cnt += 1
    if 0 == (cnt % 1000):
        print "read [%d] obj" %(cnt)
    hDomainCnt = ProcessOneObj(lvCol)
    for cate,cnt in hDomainCnt.items():
        print >>out, cate + "\t%d" %(cnt)
        
out.close()