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

from cxBase.SeparatorlineFileReader import SeparatorlineFileReaderC

class MeSHReaderC(SeparatorlineFileReaderC):
    def Init(self):
        SeparatorlineFileReaderC.Init(self)
    


