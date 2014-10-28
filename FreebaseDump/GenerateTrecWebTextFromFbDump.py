'''
Created on Oct 27, 2014 7:49:40 PM
@author: cx

what I do:
generate trec web format data for fb dump
only keep those with description
what's my input:
fb dump
what's my output:
trec web style doc.
docno = obj id
field: <name> <alias> <desp>

'''

import site
site.addsitedir("/bos/usr0/cx/PyCode/cxPyLib")
site.addsitedir("/bos/usr0/cx/PyCode/GoogleAPI")



from FreebaseDump.FbDumpBasic import FbDumpOpeC
from FreebaseDump.FbDumpReader import FbDumpReaderC


def MakeTrecWebHead(MachineId):
    Mid = MachineId.replace('.','')
#     res = ""
    res = "<DOC>\n<DOCNO>" + Mid + "</DOCNO>\n"
    res += "<DOCHDR>\nhttp://rdf.freebase.com/ns/" + MachineId + "\n</DOCHDR>\n"
    res += "<MachineId>\nMachineId" + Mid + "\n</MachineId>\n"
    return res



def MakeTextForOneObj(lvCol):
    Ope = FbDumpOpeC()
    ObjId = Ope.GetObjId(lvCol)
    lName = Ope.GetName(lvCol)
    lAlias = Ope.GetAlias(lvCol)
    desp = Ope.GetDesp(lvCol)
    
    if ("" == desp) | ([] == lName):
        return ""
    
    res = MakeTrecWebHead(ObjId)
    
    res += "<name>\n%s</name>\n" %('\n'.join(lName))
    res += "<alias>\n%s</alias>\n" %('\n'.join(lAlias))
    res += "<desp>\n%s</desp>\n" %(desp)    
    res += '</DOC>'
    return res


import sys
if 3 != len(sys.argv):
    print "fbdump + text out"
    sys.exit()
    
    
reader = FbDumpReaderC()
reader.open(sys.argv[1])
out = open(sys.argv[2],'w')

cnt = 0
for lvCol in reader:
    res = MakeTextForOneObj(lvCol)
    if "" != res:
        cnt += 1
        print >>out, res
        if 0 == (cnt % 1000):
            print "wrote [%d] obj" %(cnt)
            
out.close()