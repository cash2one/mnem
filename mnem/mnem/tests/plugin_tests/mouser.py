'''
Created on 1 Apr 2016

@author: John Beard
'''

from mnem.tests import search_tests

from mnem.plugins.electronics import MouserSearch

class FarnellTest(search_tests.SearchTest):

    def testCompOffline(self):

        cl = self.getFileTestDataLoader('mouser_uk_compl.dat')
        e = MouserSearch('uk')

        self.assertAtLeastNCompls(e, "cat", 4, compl_fetcher=cl)