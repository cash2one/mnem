'''
Created on 1 Apr 2016

@author: John Beard
'''

from mnem.tests import search_tests

from mnem.mnemory import FileCompletionLoader
from mnem.plugins import yahoo

class YahooTest(search_tests.SearchTest):

    def getFileTestDataLoader(self, name):
        '''
        Gets a data loader from the fixed test vector directory
        '''
        import os.path

        filename = os.path.join(
                                os.path.dirname(search_tests.__file__),
                                'plugin_tests', 'data', name)

        return FileCompletionLoader(filename)

    def testYahooCompOffline(self):

        cl = self.getFileTestDataLoader('yahoo_compl.dat')
        e = yahoo.YahooWebSearch(None)

        self.assertAtLeastNCompls(e, "cat", 10, compl_fetcher=cl)

    def testYahooCompOnline(self):

        e = yahoo.YahooWebSearch(None)

        self.assertAtLeastNCompls(e, "cat", 10)
