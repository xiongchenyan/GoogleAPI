'''
Created on Oct 16, 2014 3:18:32 PM
@author: cx

what I do:
spot given set of web queries
query in (not stemmed) + outname
what's my input:
qid\tquery
what's my output:
qid\tquery\tspot\tlp
'''


from TagMeAPIBase import TagMeAPIBaseC
import sys


if 3 != len(sys.argv):
    print 'query in (not stemmed) + output'
    sys.exit()
    
    
TagMeAPIBaseC().TagWebTrackQuery(sys.argv[1], sys.argv[2])

