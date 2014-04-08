'''
Created on Apr 8, 2014

@author: cx


4/8 5.00 mostly test.
tbd: different get fields
and traverse in compound neighbor (need another object)

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
#     print "[%d] results:\n%s" %(len(lFbObj),'\n'.join([json.dumps(obj.hBase) for obj in lFbObj]))
    
#     print "fetch topics for first 1"
    lFbObj = lFbObj[:3]
    for obj in lFbObj:
        obj = FetchFreebaseTopic(obj)
        print "obj [%s] topic:\n%s" %(obj.GetName(),json.dumps(obj.hTopic,indent=1))
        
#     print "get co type objects"
#     for obj in lFbObj:
#         print "obj [%s] notable [%s]" %(obj.GetName(),obj.GetNotableType())
#         lCoTypeObj = FetchTypeInstance(obj.GetNotableType(),10)
#         print "cotype obj:\n%s" %('\n'.join(lCoTypeObj))
    
    
    for obj in lFbObj:
#         print "obj [%s]" %(obj.GetName())
        for Neighbor in obj.GetNeighbor():
            print "edge:%s\nobj:[%s][%s]" %(json.dumps(Neighbor[0]),
                                            Neighbor[1].GetName().encode('utf-8','ignore'),
                                            Neighbor[1].GetId().encode('utf-8','ignore'))
        print "alias [%s]" %(json.dumps(obj.GetAlias()))
        print "name topic [%s]" %(obj.GetNameViaTopic().encode('utf-8','ignore'))
        print "type [%s]" %(json.dumps(obj.GetType()))
        
    return True



import sys

if 2 != len(sys.argv):
    print "1 para: to test query"
    sys.exit()
    
    
UnitRunQuery(sys.argv[1])

print "finished"    