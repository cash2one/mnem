
import unittest
from mnem.completion import FileCompletionLoader

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
