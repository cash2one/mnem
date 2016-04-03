'''
Created on 1 Apr 2016

@author: John Beard
'''

from mnem.tests import search_tests

from mnem.plugins import yahoo

class YahooTest(search_tests.SearchTest):

    def testYahooCompOffline(self):

        cl = self.getFileTestDataLoader('yahoo_compl.dat')
        e = yahoo.YahooWebSearch(None)

        self.assertAtLeastNCompls(e, "cat", 10, compl_fetcher=cl)

    def testYahooCompOnline(self):

        e = yahoo.YahooWebSearch(None)

        self.assertAtLeastNCompls(e, "cat", 10)
