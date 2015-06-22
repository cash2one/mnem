
import unittest

from plugins import google

MIN_RESULTS = 5;

def getsResults(engine, locale, query, num):

    e = engine(locale)
    c = e.submitForSuggestions(query)
    #print c
    return c is not None and len(c) > MIN_RESULTS


class GoogleTest(unittest.TestCase):


    def expectNResults(num=MIN_RESULTS):
        def expectSomeResults(f):
            def func_wrapper(s):
                elq = f(s)
                s.failUnless(getsResults(elq[0], elq[1], elq[2], num))
            return func_wrapper
        return expectSomeResults

    @expectNResults
    def testGoogle():
        return google.GoogleSearch, 'uk', 'cat'

    @expectNResults
    def testGFin(self):
        return google.GoogleFinanceSearch, 'uk', 'dra'

    @expectNResults(10)
    def testGImg(self):
        return google.GoogleImageSearch, 'uk', 'cat'

    @expectNResults(5)
    def testGTrends(self):
        return google.GoogleTrendsSearch, 'uk', 'cat'



def main():
    unittest.main()

if __name__ == '__main__':
    main()
