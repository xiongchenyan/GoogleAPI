'''
Created on Sep 9, 2015 3:18:04 PM
@author: cx

what I do:
    I only keep those obj's vector if it is in cached dir
what's my input:
    gensim format word2vec
    obj cache dir
what's my output:
    a filterred fb2vec file

'''


import os
import ntpath

def GetAllObjIdInCache(InDir):
    lFName = []
    for dirname,dirnames,filenames in os.walk(InDir):
        for filename in filenames:
            lFName.append(dirname + "/" + filename)
    sObjId = set([ntpath.basename(fname).replace('_','/') for fname in lFName])
    return sObjId


def FilterWord2Vec(InName,OutName,sTerm):
    ResCnt = 0
    
    print 'checking how many to keep, target [%d]' %(len(sTerm))
    for line in open(InName):
        if line.strip().split()[0] in sTerm:
            ResCnt += 1
            
    print 'keep [%d] fb2vec' %(ResCnt)            
    out = open(OutName,'w')
    
    print 'start dumpping'
    for LineCnt,line in enumerate(open(InName)):
        line = line.strip()
        if LineCnt == 0:
            print >> out,'%d\t%s' %(ResCnt, line.split()[-1])
            continue
        
        if line.split()[0] in sTerm:
            print >>out, line
        
    out.close()
    print 'dummped'
    return

    
if __name__ == '__main__':
    import sys
    
    if 4 != len(sys.argv):
        print 'I filter out fb2vec to only keep those in cache dir'
        print '3para: fb2vec in + obj cache + out'
        sys.exit()
        
        
    sObjId = GetAllObjIdInCache(sys.argv[2])
    FilterWord2Vec(sys.argv[1], sys.argv[3], sObjId)

        
