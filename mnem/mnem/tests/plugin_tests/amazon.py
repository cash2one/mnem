'''
Created on 1 Apr 2016

@author: John Beard
'''

from mnem.tests import search_tests

from mnem.plugins import amazon

class AmazonTest(search_tests.SearchTest):

    def testAmazonCompOffline(self):

        cl = self.getFileTestDataLoader('amazon_compl.dat')
        e = amazon.AmazonSearch('uk')

        self.assertAtLeastNCompls(e, "cat", 10, compl_fetcher=cl)