'''
Created on 3 Apr 2016

@author: John Beard
'''

import requests
from urllib.parse import quote

from mnem.mnem import MnemError


class CompletionError(MnemError):
    pass


class CompletionNotAvailableError(CompletionError):
    """Exception raised when a completion is not available
    """

    def __init__(self, completion):
        self.completion = completion

    def __str__(self):
        return self.completion

    def getCompletion(self):
        return self.completion


class CompletionFetchError(CompletionError):

    def __init__(self, engine, url, query, exception=None):
        self.engine = engine
        self.url = url
        self.query = query
        self.exception = exception

    def __str__(self):
        s = "%s\n%s\n%s" % (self.engine, self.url, self.query)

        if self.exception:
            s += '\n%s' % self.exception

        return s


class CompletionParseError(CompletionError):

    def __init__(self, engine, data, innerExcept):
        self.data = data
        self.engine = engine
        self.innerExcept = innerExcept

    def __str__(self):
        return "%s\n%s\n%s" % (self.engine, self.data, self.innerExcept)


class CompletionDataLoader(object):

    def _load(self):
        '''
        Perform the completion load - inheritors have to provide this
        '''
        raise NotImplementedError

class UrlCompletionDataLoader(CompletionDataLoader):
    '''
    Simple loader for inpterpolating a string into a URL and fetching
    '''

    def __init__(self, pattern):
        self.pattern = pattern

    def _load(self, query):
        '''
        Interpolate the query into the URL pattern and fetch
        '''

        try:
            data = requests.get(self.pattern % quote(query), timeout=5)
            data.close()
        except Exception as e:
            raise CompletionFetchError(self, self.pattern, query, exception=e)

        return data.text

class FileCompletionLoader(CompletionDataLoader):
    '''
    Really simple loader for loading completions from a fixed file. Probably
    mostly useful for tests
    '''

    def __init__(self, filename):
        self.fn = filename

    def _load(self, filename):

        f = open(self.fn, 'r')
        data = f.read()
        f.close()

        return data
