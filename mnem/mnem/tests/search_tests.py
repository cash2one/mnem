
import unittest
from mnem.completion import FileCompletionLoader

import os

DEFAULT_MIN_RESULTS = 5;

class SearchTest(unittest.TestCase):

    DBG_NONE = 0
    DBG_ERROR = 1
    DBG_WARNING = 2
    DBG_INFO = 3
    DBG_DEBUG = 4
    DBG_VERBOSE = 5

    @classmethod
    def getDebugLevel(c):

        key = 'MNEM_TEST_VERBOSITY'

        try:
            level = int(os.environ[key])

            if level < c.DBG_NONE or level > c.DBG_VERBOSE:
                raise ValueError
        except KeyError:
            level = c.DBG_ERROR
        except ValueError:
            raise ValueError("Test verbosity env var %s must be integer from 0-5, have '%s'" % (key, os.environ[key]))

        return level

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
