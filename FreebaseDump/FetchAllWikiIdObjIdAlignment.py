'''
Created on Nov 26, 2015 2:47:10 PM
@author: cx

what I do:
    I fetch all obj id wiki id alignment
what's my input:
    fb dump
what's my output:
    wiki id \t obj \t \t fb name

'''

import site

site.addsitedir("/bos/usr0/cx/PyCode/cxPyLib")
site.addsitedir("/bos/usr0/cx/PyCode/GoogleAPI")

from ObjCenter.FbObjBase import FbObjC
from FbDumpReader import FbDumpReaderC
from FbDumpBasic import FbDumpOpeC




def Process(FbDumpIn,OutName):
    
    reader = FbDumpReaderC()
    reader.open(FbDumpIn)
    
    out = open(OutName,'w')
    print 'start fetch all wiki id from [%s]' %(FbDumpIn)
    for cnt,lvCol in enumerate(reader):
        FbObj = FbObjC()
        FbObj.FormFromDumpData(lvCol)
        WikiId = FbObj.GetWikiId()
        if "" == WikiId:
            continue
        
        ObjId = FbObj.GetId()
        name = FbObj.GetName()
        print >>out, WikiId + '\t' + ObjId + '\t' + name
        
        if 0 == (cnt % 1000):
            print "processed [%d] obj" %(cnt)
        
    out.close()
    
    


import sys    
if 3 != len(sys.argv):
    print "I fetch wiki id alignment from dump"
    print "fb dump in + out"
    sys.exit()
    
    
Process(sys.argv[1],sys.argv[2])
print 'finished'
    
    
    
    
