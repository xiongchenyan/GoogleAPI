'''
Created on Dec 18, 2014 4:25:38 PM
@author: cx

what I do:
match q->doc->MeSH
what's my input:
qid\tquery
what's my output:
qid\tquery\tUI\tterm\tOhsumed\tscore

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from IndriSearch.IndriSearchCenter import IndriSearchCenterC
import pickle

from cxBase.Conf import cxConfC
import sys,json,math


if 2 != len(sys.argv):
    IndriSearchCenterC.ShowConf()
    print "in\nout\nohsumeddocmeshdict"
    sys.exit()

Searcher = IndriSearchCenterC(sys.argv[1])
conf = cxConfC(sys.argv[1])
InName = conf.GetConf('in')
OutName = conf.GetConf('out')
DocMeshDictIn = conf.GetConf('ohsumeddocmeshdict')

print "loading doc->mesh"
hDocAna = pickle.load(open(DocMeshDictIn))

out = open(OutName,'w')


hTermScore = {} #UI\tterm->score
for line in open(InName):
    qid,query = line.strip().split('\t')
    lDoc = Searcher.RunQuery(query)[:10]
    for doc in lDoc:
        if not doc.DocNo in hDocAna:
            continue
        lTermWithUI = hDocAna[doc.DocNo]
        for UI,term in lTermWithUI:
            key = UI + '\t' + term
            score = math.exp(doc.score)
            if not key in hTermScore:
                hTermScore[key] = score
            else:
                hTermScore[key] += score
                
    for key,score in hTermScore.items():
        print >>out, qid + '\t' + query + '\t' + key + '\tohsumed\t%f' %(score)
        
out.close()
    

    
    
