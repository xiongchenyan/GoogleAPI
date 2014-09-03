'''
Created on Sep 3, 2014
input: web query + facc annotated provided by Google
output: qid\tquery\tobj id \t obj name (in description) + score
@author: cx
'''

import sys

def LoadQ(InName):
    hQ = {}
    for line in open(InName):
        qid,query = line.strip().split('\t')
        hQ[qid] = query
    return hQ

def ProcessFaccAnaQ(hQ,InName,OutName):
    '''
    if this line is topic-n-description then following is the annotation
    until an empty line
    '''
    
    IsAnaFlag = False
    
    out = open(OutName,'w')
    
    ThisQid = ''
    for line in open(InName):
        line = line.strip()
        if ('description' in line) & ('topic' in line):
            ThisQid = line.split('-')[1]
            IsAnaFlag = True
            continue
        if len(line) == 0:
            IsAnaFlag = False
            continue
        if IsAnaFlag:
            vCol = line.split('\t')
            name = vCol[0]
            Mid = vCol[3]
            score = vCol[4]
            print >>out, ThisQid + '\t' +  hQ[ThisQid] + '\t' +  Mid + '\t' + name + '\t' + score
        
    out.close()
    
    
if 4 != len(sys.argv):
    print "query + annotated facc data + output"
    sys.exit()
    
    
hQ = LoadQ(sys.argv[1])
ProcessFaccAnaQ(hQ,sys.argv[2],sys.argv[3])
        
