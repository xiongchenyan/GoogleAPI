'''
Created on Jan 8, 2015 3:39:47 PM
@author: cx

what I do:
read record from MeSH raw data
what's my input:

what's my output:


'''



import site
site.addsitedir("/bos/usr0/cx/PyCode/cxPyLib")

from cxBase.KeyFileReader import KeyFileReaderC

class MeSHReaderC(KeyFileReaderC):
    def Init(self):
        KeyFileReaderC.Init(self)
        self.Spliter = '='
    
    def ReadNextKey(self):
        lvCol = [] #one object's all pairs
        cnt = 0
        for line in self.InFile:
            if '*NEWRECORD' in line:
                break
            vCol = line.strip().split(self.Spliter)
            
            if [] == vCol:
                continue
            vCol = [item.strip() for item in vCol]
            if cnt < self.MaxLinePerKey:
                lvCol.append(vCol)
            cnt += 1
        return lvCol
