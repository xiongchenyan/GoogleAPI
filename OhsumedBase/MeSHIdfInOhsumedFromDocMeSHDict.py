'''
Created on Dec 22, 2014 5:20:22 PM
@author: cx

what I do:
I get the idf of mesh term from the doc->MeSH ana dict
what's my input:
DocMeSHDict
what's my output:
termctf.dump

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from IndriRelate.CtfLoader import TermCtfC

import sys
import pickle

if 3 != len(sys.argv):
    print "DocMeSHDict + outname"
    sys.exit()
    
hDocMeSH = pickle.load(open(sys.argv[1]))

CtfCenter = TermCtfC()

for DocNo,lAna in hDocMeSH.items():
    for UI,term in lAna:
        CtfCenter.insert(UI)
        
CtfCenter.dump(sys.argv[2])
print "done"
