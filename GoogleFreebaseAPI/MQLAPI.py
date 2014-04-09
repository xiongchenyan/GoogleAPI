'''
Created on Apr 7, 2014
use mql api
@author: cx
'''



from APIBase import APIKey

import json,urllib,random
MqlUrl = 'https://www.googleapis.com/freebase/v1/mqlread'



def CreateMqlPara():
    return {'key':random.choice(APIKey)
            }
    
    
def FetchTypeInstance(TypeName,NumOfInstance=100):
    #input type name
    #return a list of object id
    query = [{'id':None,'type':TypeName}]
    params = CreateMqlPara()
    params['query'] = json.dumps(query)
    
    url = MqlUrl + '?' + urllib.urlencode(params)
    CursorIndex = ""
    lInstanceId = []
    while len(lInstanceId) < NumOfInstance:
        CursorStr = ""
        if CursorIndex != "":
            CursorStr = "=" + CursorIndex
        print "mql api url [%s]" %(url)
        response = json.loads(urllib.urlopen(url + "&cursor" + CursorStr).read())
#         print "mql res:\n%s" %(json.dumps(response))

        if not 'result' in response:
            print "no result in mql quuery"
            return []

        for result in response['result']:
            if 'id' in result:
                lInstanceId.append(result['id'])
        
        if 'cursor' in response:
            CursorIndex = response['cursor']
            if (not CursorIndex) | (CursorIndex == 'false'):
                break    
    return lInstanceId[:NumOfInstance]
            