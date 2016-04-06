'''
Created on 3 Apr 2016

@author: John Beard
'''

import requests
from urllib.parse import quote
from mnem import mnem


class RequestDataLoadError(mnem.MnemError):
    '''
    Error thrown when a request fails to acquire required data
    '''

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


class RequestDataLoader(object):

    def load(self):
        '''
        Perform the completion load - inheritors have to provide this
        '''
        raise NotImplementedError

class UrlCompletionDataLoader(RequestDataLoader):
    '''
    Simple loader for inpterpolating a string into a URL and fetching
    '''

    def __init__(self, pattern):
        self.pattern = pattern

    def load(self, query):
        '''
        Interpolate the query into the URL pattern and fetch
        '''

        try:
            data = requests.get(self.pattern % quote(query), timeout=5)
            data.close()
        except Exception as e:
            raise RequestDataLoadError(self, self.pattern, query, exception=e)

        return data.text

class FileCompletionLoader(RequestDataLoader):
    '''
    Really simple loader for loading completions from a fixed file. Probably
    mostly useful for tests
    '''

    def __init__(self, filename):
        self.fn = filename

    def load(self, filename):

        f = open(self.fn, 'r')
        data = f.read()
        f.close()

        return data

