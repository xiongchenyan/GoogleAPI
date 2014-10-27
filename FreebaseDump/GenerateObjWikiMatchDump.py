'''
Created on Oct 27, 2014 7:27:14 PM
@author: cx

what I do:
run FbObjWikiMatch.GenerateDictDump
what's my input:

what's my output:


'''



import site
site.addsitedir("/bos/usr0/cx/PyCode/cxPyLib")
site.addsitedir("/bos/usr0/cx/PyCode/GoogleAPI")

from FreebaseDump.FbObjWikiMatch import FbObjWikiMatchC


import sys
if len(sys.argv) != 2:
    FbObjWikiMatchC.ShowConf()
    sys.exit()
    
    
Processor = FbObjWikiMatchC(sys.argv[1])
Processor.GenerateDictDump()

