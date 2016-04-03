'''
Created on 1 Apr 2016

@author: John Beard
'''

from mnem.tests import search_tests

from mnem.plugins import wolframalpha

class WolframAlphaTest(search_tests.SearchTest):

    def testEnwikiCompOffline(self):

        cl = self.getFileTestDataLoader('wolframalpha_compl.dat')
        e = wolframalpha.WolframAlphaSearch()

        self.assertAtLeastNCompls(e, "cat", 10, search_loader=cl)