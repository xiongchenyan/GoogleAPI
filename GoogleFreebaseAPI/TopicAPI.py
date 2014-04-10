'''
Created on Apr 7, 2014
fill the hTopic dict in object via topic API
@author: cx
'''


from APIBase import APIKey

import json,urllib,random
TopicUrl = 'https://www.googleapis.com/freebase/v1/topic'

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
    topic = json.loads(urllib.urlopen(url).read())
    if 'property' in topic:
        FbApiObj.hTopic = dict(FbApiObj.hTopic.items() + topic['property'].items())
    else:
        print "fill by topic api return res error [%s]" %(json.dumps(topic))
    return FbApiObj
    
