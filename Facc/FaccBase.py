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

import json

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


    def __init__(self,data = "",Type = 'facc'):
        self.Init()
        if "" != data:
            self.loads(data,Type)
        
    def loads(self,line,Type = 'facc'):
        vCol = line.strip().split('\t')
        if Type == 'facc':
            return self.LoadsFacc(vCol)
        else:
            return self.LoadsFakba(vCol)
        
        print "[%s] [%d] col not valid facc/fakba line" %(line,len(vCol))
        return False
    
    def LoadsFacc(self,vCol):
        if len(vCol) < 8:
            return False
        try:
            self.DocNo = vCol[0]
            self.EnCoding = vCol[1]
            self.entity = vCol[2]
            self.st = int(vCol[3])
            self.ed = int(vCol[4])
            self.Prob = float(vCol[5])
            self.ContextProb = float(vCol[6])
        except ValueError:
            print "facc line parse error"
            self.ObjId = "" #sign of failure
            return False
        self.ObjId = vCol[7]
        return True
        
    def LoadsFakba(self,vCol):
        if len(vCol) < 7:
            return False 
        try:
            self.DocNo,self.entity,self.st,self.ed,self.Prob,self.ContextProb,self.ObjId = vCol[:7]
            self.st = int(self.st)
            self.ed = int(self.ed)
            self.Prob = float(self.Prob)
            self.ContextProb = float(self.ContextProb)
        except ValueError:
            print "fakba line  parse error"
            self.ObjId = ""   #sign of failure
            return False
        return True
        
        
    def dumps(self):
        res = self.DocNo + "\t" + self.EnCoding + "\t" + self.entity
        res += "\t%d\t%d\t%f\t%f\t" %(self.st,self.ed,self.Prob,self.ContextProb)
        res += self.ObjId
        return res
    
    

    
    
    
        