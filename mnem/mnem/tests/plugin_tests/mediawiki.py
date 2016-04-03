'''
Created on 1 Apr 2016

@author: John Beard
'''

from mnem.tests import search_tests

from mnem.plugins import mediawiki

class MediawikiTest(search_tests.SearchTest):

    def testEnwikiCompOffline(self):

        cl = self.getFileTestDataLoader('wikipedia_en_compl.dat')
        e = mediawiki.WikipediaSearch('en')

        self.assertAtLeastNCompls(e, "cat", 10, search_loader=cl)

    def testEnwikiCompOnline(self):

        e = mediawiki.WikipediaSearch('en')
        self.assertAtLeastNCompls(e, "cat", 10)
