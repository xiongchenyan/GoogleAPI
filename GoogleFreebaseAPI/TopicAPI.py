'''
Created on Apr 7, 2014
fill the hTopic dict in object via topic API
@author: cx
'''


from APIBase import APIKey

import json,urllib,random
TopicUrl = 'https://www.googleapis.com/freebase/v1/topic'
import time
def CreateTopicPara():
    params = {
              'key': random.choice(APIKey),
              'filter': 'commons'
              }
    return params


def FetchFreebaseTopic(FbApiObj):
    Mid = FbApiObj.GetId()
    if "" == Mid:
        return FbApiObj
    
    url = TopicUrl +  Mid + "?" + urllib.urlencode(CreateTopicPara())
    print "topic api fetching url [%s]" %(url)
    
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
    topic = json.loads(data)
    
    time.sleep(0.1)
    if 'property' in topic:
        FbApiObj.hTopic = dict(FbApiObj.hTopic.items() + topic['property'].items())
    else:
        print "fill by topic api return res error [%s]" %(json.dumps(topic))
    return FbApiObj
    
