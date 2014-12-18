'''
Created on Dec 18, 2014 2:13:42 PM
@author: cx

what I do:
get the annotation for all docs and dump to dict
what's my input:
Ohsumed raw doc
MeSHTermDict
what's my output:
dump dict by pickle to be used as doc->MeSH Terms mapping

'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
import pickle

import sys
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from OhsumedBase.OhsumedDocMeSHAnaCenter import OhsumedDocMeSHAnaCenterC

if 2 != len(sys.argv):
    OhsumedDocMeSHAnaCenterC.ShowConf()
    print "docin\nout\nmeshtermdict\mtargetdocno"
    sys.exit()
    

conf = cxConfC(sys.argv[1])
DocInName = conf.GetConf('docin')
OutName = conf.GetConf('out')
MeshTermDictInName = conf.GetConf('meshtermdict')
TargetDocNoName = conf.GetConf('targetdocno')

lDocNo = open(TargetDocNoName).read().splitlines()
hTargetDocNo = dict(zip(lDocNo,[0] * len(lDocNo)))

AnaCenter = OhsumedDocMeSHAnaCenterC(sys.argv[1])
AnaCenter.FormDocMeSHDict(DocInName, MeshTermDictInName,hTargetDocNo)

print "dumping dict"
pickle.dump(AnaCenter.hDocToMeSh,open(OutName,'wb'))

print "finished"

