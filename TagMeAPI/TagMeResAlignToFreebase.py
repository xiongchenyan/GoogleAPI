'''
Created on my MAC Aug 31, 2015-10:11:53 PM
What I do:
    I aligh tagme results to fb id
What's my input:
    TagMe res (first col is docno, #-> is tag res)
    Wiki->Fb id dict output of FbObjFetcher
        each line:
            wiki id\t fb id \t name
    
What's my output:
    doc no \t tag res \t fb id \t fb name

@author: chenyanxiong
'''

import sys
import logging


def LoadWikiFbDict(InName):
    lvCol = [line.split('\t') for line in open(InName).read().splitlines()]
    
    lItems = [[item[0],'\t'.join(item[1:])] for item in lvCol]
    hWikiFb = dict(lItems)
    return hWikiFb



def AlignOneLine(line, hWikiFb):
    DocNo = line.split()[0]
    
    vTagMeCol = line.split('#')[-1].strip().split('\t')
    
    vRes = []
    for i in range(len(vTagMeCol) / 6):
        
        vTargetCol = vTagMeCol[i * 6: i * 6 + 6]
        
        FbId = "None"
        FbName = "Null"
        WikiId = vTargetCol[0]
        if WikiId in hWikiFb:
            FbId,FbName = hWikiFb[WikiId]
            
        vRes.extend(vTargetCol + [FbId,FbName])
        
    return '\t'.join([DocNo] + vRes)


def Process(TaggedDataIn, WikiFbInforIn,OutName):
    
    hWikiFb = LoadWikiFbDict(WikiFbInforIn)
    
    out = open(OutName,'w')
    
    for cnt,line in enumerate(open(TaggedDataIn)):
        print>> out, AlignOneLine(line.strip(), hWikiFb)
        if 0 == (cnt % 1000):
            print 'processed [%d] lines' %(cnt)
        
    out.close()
    print 'finished'
    
    
    
if 4 != len(sys.argv):
    print 'I align tagme res to fb obj id-name, with the infor provided via FbObjFetcher'
    print '3 para: TagMe res in + wiki-fb data in  + output'
    sys.exit()
    
    
Process(sys.argv[1],sys.argv[2],sys.argv[3])
        
        
