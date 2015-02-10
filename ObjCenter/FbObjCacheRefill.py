'''
Created on Feb 10, 2015 2:19:16 PM
@author: cx

what I do:
There are some cached objects with only hBase, not hTopic.
I am going to fetch the hTopic for them
what's my input:
Cache Dir
what's my output:
for all obj id in cache, I will refetch it

'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from ObjCenter.FbObjCacheCenter import *
from cxBase.Conf import cxConfC
import sys

if 2 != len(sys.argv):
    FbObjCacheCenterC.ShowConf()
    sys.exit()
    
CacheCenter = FbObjCacheCenterC(sys.argv[1])
DumpCnt = 0
for ObjId in CacheCenter.hObj.keys():
    ApiObj = CacheCenter.FetchObj(ObjId)
    if {} == ApiObj.hTopic:
        ApiObj = FetchFreebaseTopic(ApiObj)
        ApiObj.dump(CacheCenter.GetDirForObj(ObjId))
        print '[%s] dumped [%d]' %(ObjId,DumpCnt)
        DumpCnt += 1
        
print '%d/%d redumped\n' %(DumpCnt,len(CacheCenter.hObj))

            


