
import unittest
from mnem.mnemory import FileCompletionLoader

DEFAULT_MIN_RESULTS = 5;

class SearchTest(unittest.TestCase):

    def getFileTestDataLoader(self, name):
        '''
        Gets a data loader from the fixed test vector directory
        '''
        import os.path

        filename = os.path.join(os.path.dirname(__file__),
                                'plugin_tests', 'data', name)

        return FileCompletionLoader(filename)

    def getCompls(self, engine, query, completion=None, compl_fetcher=None):

        if compl_fetcher:
            engine.setCompletionLoader(compl_fetcher)

        comps = engine.availableCompletions()
        if comps:
            c = engine.submitForSuggestions(comps[0], query)
        else:
            c = None

        return c

    def assertAtLeastNCompls(self, engine, query, num,
                                 completion=None, compl_fetcher=None):
        """
        Asserts that the given engine and parameters returns at least this
        many results
        """
        c = self.getCompls(engine, query, completion, compl_fetcher)

        self.assertTrue(c is not None)
        self.assertGreaterEqual(len(c), num)



def expectNResults(num=DEFAULT_MIN_RESULTS):
    def expectSomeResults(f):
        def func_wrapper(s):
            elq = f(s)
            s.assertTrue(getsResults(elq[0], elq[1], elq[2], num))
        return func_wrapper
    return expectSomeResults

def getsResults(engine, locale, query, num):

    e = engine(locale)

    comps = e.availableCompletions()
    if comps:
        c = e.submitForSuggestions(comps[0], query)
    else:
        c = None

    return c is not None and len(c) > num

def fetch_offline_data(filename):

    def get_data():
        return open(filename, 'r').read()

    return get_data
