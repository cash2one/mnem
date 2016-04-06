'''
Created on 1 Apr 2016

@author: John Beard
'''

from mnem.tests import search_tests

from mnem.plugins import google

class GoogleTest(search_tests.SearchTest):

    def testGoogle(self):
        self.assertAtLeastNCompls(google.GoogleSearch(),
                                      "cat", 5)

    def testGoogleFin(self):
        self.assertAtLeastNCompls(google.GoogleFinanceSearch(),
                                      "dra", 5)

    def testGoogleImg(self):
        self.assertAtLeastNCompls(google.GoogleImageSearch(),
                                      "cat", 10)

    def testGoogleTrends(self):
        self.assertAtLeastNCompls(google.GoogleTrendsSearch(),
                                      "cat", 5)
