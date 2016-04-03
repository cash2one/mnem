'''
Created on 1 Apr 2016

@author: John Beard
'''

from mnem.tests import search_tests

from mnem.plugins.electronics import OctopartSearch

class OctopartTest(search_tests.SearchTest):

    def testCompOffline(self):

        cl = self.getFileTestDataLoader('octopart_compl.dat')
        e = OctopartSearch()

        self.assertAtLeastNCompls(e, "cat", 10, search_loader=cl)