'''
Created on Apr 22, 2014

@author: cx
'''



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
        vCol = line.strip('\t')
        if len(vCol) != 8:
            print "[%s] not valid facc line" %(line)
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
    
    

        
        
