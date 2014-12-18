'''
Created on Dec 18, 2014 1:48:24 PM
@author: cx

what I do:
I tag MeSH term by:
tagme->wiki entity ->mapping the MeSH using exact match
what's my input:
qid\tquery
what's my output:
qid\tquery\tUI\tterm\tPubMed\t1

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from MeSHBase.TagMeMeSHAnnotator import TagMeMeSHAnnotatorC
import sys
from cxBase.Conf import cxConfC

if 2 != len(sys.argv):
    TagMeMeSHAnnotatorC.ShowConf()
    print "in\nout"
    sys.exit()
    
conf = cxConfC(sys.argv[1])
InName = conf.GetConf('in')
OutName = conf.GetConf('out')
Annotator = TagMeMeSHAnnotatorC(sys.argv[1])

out = open(OutName,'w')

for line in open(InName):
    qid,query = line.strip().split('\t')
    lMeSH = Annotator.AnnotateQuery(query)
    for UI,term in lMeSH:
        print >>out,qid + "\t" + query + "\t" + UI + "\t" + term + "\tTagMe\t1.0"

out.close()
print "all finished"

