
import unittest
from mnem.completion import FileCompletionLoader

import os
from mnem import mnemory

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

    def getCompls(self, engine, query, completion_req=None,
                  search_loader=None):
        '''
        Test helper to get the completion array from a completion search
        '''

        if not completion_req:
            completion_req = engine.getDefaultCompletion()

        comps = engine.getRequestData(completion_req, {'query': query}, search_loader=search_loader)

        try:
            return comps.compls
        except AttributeError:
            return []

    def assertAtLeastNCompls(self, engine, query, num, completion_req=None,
                             search_loader=None):
        """
        Asserts that the given engine and parameters returns at least this
        many results
        
        Useful for a quick test, but better if you can check that the results
        are also correct
        """
        c = self.getCompls(engine, query, completion_req, search_loader)

        self.assertTrue(c is not None)
        self.assertGreaterEqual(len(c), num)
