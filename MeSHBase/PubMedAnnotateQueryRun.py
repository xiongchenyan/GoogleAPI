'''
Created on Dec 17, 2014 7:33:01 PM
@author: cx

what I do:
annotate q with pubmed annotator
what's my input:
qid\tquery
what's my output:
qid\tquery\tUI\tterm\tPubMed\t1
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from MeSHBase.PubMedAnnotator import PubMedAnnotatorC
import sys
from cxBase.Conf import cxConfC

if 2 != len(sys.argv):
    PubMedAnnotatorC.ShowConf()
    print "in\nout"
    sys.exit()
    
conf = cxConfC(sys.argv[1])
InName = conf.GetConf('in')
OutName = conf.GetConf('out')
Annotator = PubMedAnnotatorC(sys.argv[1])

out = open(OutName,'w')

for line in open(InName):
    qid,query = line.strip().split('\t')
    lMeSH = Annotator.AnnotateQuery(query)
    for UI,term in lMeSH:
        print >>out,qid + "\t" + query + "\t" + UI + "\t" + term + "\tPubMed\t1.0"

out.close()
print "all finished"

