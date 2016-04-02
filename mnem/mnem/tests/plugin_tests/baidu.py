'''
Created on 1 Apr 2016

@author: John Beard
'''

from mnem.tests import search_tests

from mnem.plugins import baidu

class BaiduTest(search_tests.SearchTest):

    def testWebCompOffline(self):

        cl = self.getFileTestDataLoader('baidu_web_compl.dat')
        e = baidu.BaiduWebSearch()

        self.assertAtLeastNCompls(e, "cat", 10, compl_fetcher=cl)

    def testImgCompOffline(self):

        cl = self.getFileTestDataLoader('baidu_image_compl.dat')
        e = baidu.BaiduImageSearch()

        self.assertAtLeastNCompls(e, "cat", 10, compl_fetcher=cl)
