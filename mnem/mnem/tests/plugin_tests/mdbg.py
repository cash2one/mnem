'''
Created on 6 Apr 2016

@author: John Beard
'''


from mnem.tests import search_tests

from mnem.plugins import mdbg

class MdbgTest(search_tests.SearchTest):

    def testMdbgCompOffline(self):

        cl = self.getFileTestDataLoader('mdbg_compl.dat')
        e = mdbg.MdbgSearch()

        self.assertAtLeastNCompls(e, "cat", 10, search_loader=cl)
