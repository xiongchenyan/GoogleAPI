'''
Created on May 30, 2014
input: word2vec file + list of terms
output: lWord2VecC
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
from word2vec.WordVecBase import *

def WordVecBatchFetcher(lTerm,Word2vecInName):
    Reader = Word2VecReaderC()
    Reader.open(Word2vecInName)
    hTerm = dict(zip(lTerm,[0]*len(lTerm)))
    print "fetching word2vec for [%d] terms" %(len(hTerm))
    
    
    cnt = 0
    for WordVec in Reader:
        cnt += 1
        if 0 == (cnt % 10000):
            print "[%d] line" %(cnt)
        if WordVec.word in hTerm:
            print "get word [%s]" %(WordVec.word)
            hTerm[WordVec.word] = WordVec
    
    lWord2Vec = []
    for term in lTerm:
        if hTerm[term] != 0:
            lWord2Vec.append(hTerm[term])
        else:
            lWord2Vec.append(Word2VecC())
            
    return lWord2Vec
    