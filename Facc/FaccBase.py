'''
Created on Apr 22, 2014



@author: cx
'''


'''
May 19 2014
add a document level class to store all facc of a doc
add a query level read/write function

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from Facc.FaccReader import FaccReaderC

class FaccAnnotationC(object):
    def Init(self):
        self.DocNo = ""
        self.EnCoding = ""
        self.entity = ""
        self.st = 0
        self.ed = 0
        self.Prob = 0
        self.ContextProb = 0
        self.ObjId = ""


    def __init__(self,data = ""):
        self.Init()
        if "" != data:
            self.loads(data)
        
    def loads(self,line):
        vCol = line.strip().split('\t')
        if len(vCol) != 8:
            print "[%s] [%d] col not valid facc line" %(line,len(vCol))
            return False
        self.DocNo = vCol[0]
        self.EnCoding = vCol[1]
        self.entity = vCol[2]
        self.st = int(vCol[3])
        self.ed = int(vCol[4])
        self.Prob = float(vCol[5])
        self.ContextProb = float(vCol[6])
        self.ObjId = vCol[7]
        return True
    
    def dumps(self):
        res = self.DocNo + "\t" + self.EnCoding + "\t" + self.entity
        res += "\t%d\t%d\t%f\t%f\t" %(self.st,self.ed,self.Prob,self.ContextProb)
        res += self.ObjId
        return res
    
    

        
        
class FaccForDocC(object):
    def Init(self):
        self.lFacc = []
        self.DocNo = ""
        
    def __init__(self,lFacc = []):
        self.Init()
        if [] != lFacc:
            self.Set(lFacc)
            
    def Set(self,lFacc):
        self.lFacc = list(lFacc)
        self.DocNo = lFacc[0].DocNo
        
    def dumps(self):
        res = ""
        for facc in self.lFacc:
            res += facc.dumps() + "\n"
        return res.strip()
    
    
    @staticmethod
    def ReadFaccDocs(InName):
        Reader = FaccReaderC()
        Reader.open(InName)
        lFaccDoc = []
        for lFacc in Reader:
            lFaccDoc.append(FaccForDocC(lFacc))
        return lFaccDoc
    
    @staticmethod
    def DumpFaccDocs(lFaccDoc, OutName):
        out = open(OutName,'w')
        for FaccDoc in lFaccDoc:
            print >>out, FaccDoc.dumps()
        out.close()
        return True
        
    
    
    
    
        