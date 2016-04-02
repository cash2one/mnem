'''
Created on 1 Apr 2016

@author: John Beard
'''

from mnem.tests import search_tests

from mnem.plugins.electronics import FarnellSearch

class FarnellTest(search_tests.SearchTest):

    def testCompOffline(self):

        cl = self.getFileTestDataLoader('farnell_uk_compl.dat')
        e = FarnellSearch('uk')

        self.assertAtLeastNCompls(e, "cat", 8, compl_fetcher=cl)