'''
Created on 1 Apr 2016

@author: John Beard
'''

from mnem.tests import search_tests

from mnem.plugins.farnell import FarnellSearch

class FarnellTest(search_tests.SearchTest):

    def testCompOffline(self):

        cl = self.getFileTestDataLoader('farnell_uk_compl.dat')
        e = FarnellSearch('uk')

        self.assertAtLeastNCompls(e, "cat", 8, compl_fetcher=cl)

    def testCompShortQuery(self):

        e = FarnellSearch('uk')

        # should detect the short query and short circuit
        c = self.getCompls(e, "ca")

        self.assertEqual(0, len(c), "Expected to short circuit on short query")
