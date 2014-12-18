'''
Created on Oct 16, 2014 2:55:48 PM
@author: cx

what I do:
call TagMeAPI to fetch results.
Spotting and Tagging.
Prefer to use Spotting now as tagging leads to Wikipedia. 
what's my input:
query
what's my output:
Spotting:
    list[hSpot]
    hSpot = {'lp':'score','spot':'text,'start':int,'end':int}
Tagging:
    not defined yet
'''

'''
Oct 28 Add tag API support
Tagging:
in:
    query
output:
    lhAnnotation = [{hAna}]
    hAna: 'abstract' 'title' 'spot' 'rho' (confidence, default choose >0.1)
'''


import json
import urllib
import time
class TagMeAPIBaseC(object):
    def __init__(self):
        self.APIKey = "d252540aaf6a9ee8457db5212e543189"
        self.SpotUrl = 'http://tagme.di.unipi.it/spot'
        self.TagUrl = 'http://tagme.di.unipi.it/tag'
    
    
    def FetchUrlData(self,url):
        cnt = 0
        data = ""
        while (cnt < 10):
            try:
                data = urllib.urlopen(url).read()
            except IOError:
                time.sleep(1)
                print "IOError, wait [%d] time" %(cnt)
                cnt += 1
                continue
            break    
        return data
    
    def TagText(self,text):
        hPara = {}
        hPara['key'] = self.APIKey
        hPara['text'] = text
        hPara['include_abstract'] = True
        
        url = self.TagUrl + '?' + urllib.urlencode(hPara)
        response = json.loads(self.FetchUrlData(url))
        if not 'annotations' in response:
            return []
        return response['annotations']
    
    def TagMulText(self,lText):
        return [self.TagText(text) for text in lText]
    
    def TagWebTrackQuery(self,QueryInName,OutName):
        out = open(OutName,'w')
        for line in open(QueryInName):
            query = line.strip().split('\t')[1]
            lhAna = self.TagText(query)
            print >>out, line.strip() + '\t' + json.dumps(lhAna,indent=1) + '\n'
        out.close()
        
    def SpotForText(self,text):
        hPara = {}
        hPara['key'] = self.APIKey
        hPara['text'] = text
        
        url = self.SpotUrl + "?" + urllib.urlencode(hPara)
        data = self.FetchUrlData(url)    
        response = json.loads(data)
        if not "spots" in response:
            return []
        
        return response['spots']
    
    
    def SpotForMultipleText(self,lText):
        return [self.SpotForText(text) for text in lText]
    
    
    def SpotWebTrackQuery(self,QueryInName,OutName):
        '''
        prefer not-stemmed queries
        qid\tquery on each line
        output:
            qid\tquery\tspot\tlp
        '''    
        EmptyCnt = 0
        lNotSpot = []
        cnt = 0
        out = open(OutName,'w')
        lQidQuery = []
        for line in open(QueryInName):
            line = line.strip()
            qid,query = line.split('\t')
            lQidQuery.append([qid,query])
        lQidQuery.sort(key=lambda item:int(item[0]))
        for qid,query in lQidQuery:
            print 'spotting [%s]' %(query)
            lhSpot = self.SpotForText(query)
            if [] == lhSpot:
                EmptyCnt += 1
                lNotSpot.append(line)
            cnt += 1
            
            for hSpot in lhSpot:
                if float(hSpot['lp']) < 0.05:
                    continue
                print >>out, qid + '\t' + query + '\t%s\t%s' %(hSpot['spot'],hSpot['lp'])
            
            
        out.close()
        print 'finished [%d]/[%d] not spotted' %(EmptyCnt,cnt)
        print json.dumps(lNotSpot,indent=1)
        
            
            
        
        
        
        
        
        
    
    
    