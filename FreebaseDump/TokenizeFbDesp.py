'''
Created on Mar 9, 2015 5:26:01 PM
@author: cx

what I do:
tokenize fb dump
what's my input:
name \t mid \t desp
what's my output:
name \t mid \t tokenzied 1 st sentence \t 2nd sentence \t 3rd sentence

'''

import nltk
import nltk.data


import sys

if 3 != len(sys.argv):
    print "desp in + output"
    sys.exit()
    

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
out = open(sys.argv[2],'w')
cnt = 0
for line in open(sys.argv[1]):
    vCol = line.strip().split('\t')
    name = vCol[0].strip('"')
    mid = vCol[1]
    desp = vCol[2]
    lSentence = sent_detector.tokenize(desp)
    llTokens = []
    for sentence in lSentence[:3]:
        lTokens = nltk.word_tokenize(sentence)
        llTokens.append(lTokens)
    lTokenStr = [' '.join(lTokens) for lTokens in llTokens]
    TokenStr = '\t'.join(lTokenStr)
    print >>out, name + '\t' + mid + '\t' + TokenStr
    cnt += 1
    if 0 == (cnt % 100):
        print "processed [%d] line" %(cnt)
        
out.close()
print "done"