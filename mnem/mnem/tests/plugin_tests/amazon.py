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

        self.assertAtLeastNCompls(e, "cat", 10, search_loader=cl)

    def testDefSearch(self):

        e = amazon.AmazonSearch('uk')

        d = e.getRequestData(e.R_DEF_SEARCH, {'query':'cat'})

        self.assertEqual("http://amazon.co.uk/s/?field-keywords=cat",
                         d.url)
