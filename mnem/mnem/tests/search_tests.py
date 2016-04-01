
import unittest

DEFAULT_MIN_RESULTS = 5;

class SearchTest(unittest.TestCase):
    pass

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

    return c is not None and len(c) > DEFAULT_MIN_RESULTS
