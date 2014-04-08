'''
Created on Apr 8, 2014

@author: cx
'''

import site
import os
import pickle
import json
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib/')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI/')
from cxBase.base import cxConf,cxBaseC
from APIBase import *
from MQLAPI import *
from SearchAPI import *
from TopicAPI import *


def UnitRunQuery(query):
    print "start search [%s]" %(query)
    lFbObj = SearchFreebase(query)
    print "[%d] results:\n%s" %(len(lFbObj),'\n'.join([json.dumps(obj.hBase) for obj in lFbObj]))
    
    print "fetch topics for first 2"
    lFbObj = lFbObj[:2]
    for obj in lFbObj:
        obj = FetchFreebaseTopic(obj)
        print "obj [%s] topic:\n%s" %(obj.GetName(),json.dumps(obj.hTopic,indent=1))
        
    print "get co type objects"
    for obj in lFbObj:
        print "obj [%s] notable [%s]" %(obj.GetName(),obj.GetNotableType())
        lCoTypeObj = FetchTypeInstance(obj.GetNotableType(),10)
        print "cotype obj:\n%s" %('\n'.join([Obj.GetName() for Obj in lCoTypeObj]))
        
    return True



import sys

if 2 != len(sys.argv):
    print "1 para: to test query"
    sys.exit()
    
    
UnitRunQuery(sys.argv[1])

print "finished"    