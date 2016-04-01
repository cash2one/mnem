'''
Created on 1 Apr 2016

@author: John Beard
'''

from mnem.tests import search_tests

from mnem.plugins import google

class GoogleTest(search_tests.SearchTest):

    @search_tests.expectNResults
    def testGoogle(self):
        return google.GoogleSearch, 'uk', 'cat'

    @search_tests.expectNResults
    def testGFin(self):
        return google.GoogleFinanceSearch, 'uk', 'dra'

    @search_tests.expectNResults(10)
    def testGImg(self):
        return google.GoogleImageSearch, 'uk', 'cat'

    @search_tests.expectNResults(5)
    def testGTrends(self):
        return google.GoogleTrendsSearch, 'uk', 'cat'