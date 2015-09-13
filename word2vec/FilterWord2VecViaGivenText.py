'''
Created on Sep 13, 2015 2:46:44 PM
@author: cx

what I do:
    I filter out a word2vec data via given terms
what's my input:
    
what's my output:


'''

from FilterFb2VecViaCachedId import FilterWord2Vec


def LoadTermsFromText(InName):
    lLines = open(InName).read().splitlines()
    lTerm = []
    for line in lLines:
        lTerm.extend(line.split())
    return set(lTerm)



if __name__ == '__main__':
    import sys
    
    if 4 != len(sys.argv):
        print 'I filter out word2vec to only keep those in give text'
        print '3para: word2vec in + text + out'
        sys.exit()
        
        
    sTerm = LoadTermsFromText(sys.argv[2])
    FilterWord2Vec(sys.argv[1], sys.argv[3], sTerm)
        
        
