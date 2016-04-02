'''
Created on 1 Apr 2016

@author: John Beard
'''

from mnem.tests import search_tests

from mnem.plugins import google

class GoogleTest(search_tests.SearchTest):

    def testGoogle(self):
        self.assertAtLeastNCompls(google.GoogleSearch,
                                      "cat", 5)

    def testGFin(self):
        self.assertAtLeastNCompls(google.GoogleFinanceSearch,
                                      "dra", 5)

    def testGImg(self):
        self.assertAtLeastNCompls(google.GoogleImageSearch,
                                      "cat", 10)

    def testGTrends(self):
        self.assertAtLeastNCompls(google.GoogleTrendsSearch,
                                      "cat", 5)
