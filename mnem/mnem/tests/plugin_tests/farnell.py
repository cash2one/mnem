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

        cs = self.getCompls(e, "scr", compl_fetcher=cl)

        self.assertEqual(12, len(cs))

        prods = [c for c in cs if c.req_type == FarnellSearch.R_PRODUCT]
        cats = [c for c in cs if c.req_type == FarnellSearch.R_CATEGORY]
        manfs = [c for c in cs if c.req_type == FarnellSearch.R_MANUFACTURER]

        # we know the number of results here
        self.assertEqual(6, len(prods))
        self.assertEqual(1, len(manfs))
        self.assertEqual(5, len(cats))

        if self.getDebugLevel() >= self.DBG_DEBUG:
            for p in cs:
                print("%s (%s)\n\t%s" % (p.keyword, p.category, p.description))

    def testCompShortQuery(self):

        e = FarnellSearch('uk')

        # should detect the short query and short circuit
        c = self.getCompls(e, "ca")

        self.assertEqual(0, len(c), "Expected to short circuit on short query")

    def testSrcProduct(self):

        e = FarnellSearch('uk')

        d = e.getRequestData(FarnellSearch.R_PRODUCT, {'query': 'scr'})

        # did we get the right url?
        self.assertEqual("http://uk.farnell.com/Search?st=scr", d.url)
