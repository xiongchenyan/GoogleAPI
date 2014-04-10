'''
Created on Apr 4, 2014

@author: cx
'''

from APIBase import APIKey,FbApiObjectC

import json,urllib
import random
import time
SearchUrl = 'https://www.googleapis.com/freebase/v1/search'

def CreateSearchPara():
    return {'key':random.choice(APIKey),'lang':'en','limit':20}

def SearchFreebase(query):
    #return a list of results
    params = CreateSearchPara()
    params['query'] = query
    
    url = SearchUrl + "?" + urllib.urlencode(params)
    print "search api url [%s]" %(url)
    cnt = 0
    data = ""
    while (cnt < 100):
        try:
            data = urllib.urlopen(url).read()
        except IOError:
            time.sleep(10)
            print "IOError, wait [%d] time" %(cnt)
            cnt += 1
            continue
        break    
    response = json.loads(data)
    time.sleep(0.5)
    if not 'OK' in response['status']:
        print "search freebase failed, check your quota"
        return []
    lObj = []
    for result in response['result']:
        APIObj = FbApiObjectC()
        APIObj.hBase = dict(result)
        lObj.append(APIObj)
    return lObj