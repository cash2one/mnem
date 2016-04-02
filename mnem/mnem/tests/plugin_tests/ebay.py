'''
Created on 1 Apr 2016

@author: John Beard
'''

from mnem.tests import search_tests

from mnem.plugins import ebay

class EbayTest(search_tests.SearchTest):

    def testEbayCompOffline(self):

        cl = self.getFileTestDataLoader('ebay_compl.dat')
        e = ebay.EbaySearch('uk')

        self.assertAtLeastNCompls(e, "cat", 10, compl_fetcher=cl)