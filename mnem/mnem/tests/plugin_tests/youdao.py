'''
Created on 1 Apr 2016

@author: John Beard
'''

from mnem.tests import search_tests

from mnem.plugins import youdao

class YoudaoTest(search_tests.SearchTest):

    def testCompOffline(self):

        cl = self.getFileTestDataLoader('youdao_compl.dat')
        e = youdao.YouDaoDictSearch()

        self.assertAtLeastNCompls(e, "cat", 8, search_loader=cl)