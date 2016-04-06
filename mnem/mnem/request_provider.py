'''
Created on 6 Apr 2016

@author: John Beard
'''

from mnem import request_data, request_loader
from mnem.mnem import MnemError


class RequestDataError(MnemError):
    '''
    Exception thrown when returned data cannot be parsed into meaninfuul results
    '''

    def __init__(self, engine, data, innerExcept):
        self.data = data
        self.engine = engine
        self.innerExcept = innerExcept

    def __str__(self):
        return "%s\n%s\n%s" % (self.engine, self.data, self.innerExcept)

class RequestProvider(object):

    def execute_request(self, opts):

        if not self._can_process_query(opts):
            return None

        data = self._load_data(opts)
        return self._process_data(opts, data)

    def _can_process_query(self, opts):
        '''
        Override if the provider can tell upfront if a query isn't suitable
        '''
        return True

    def set_loader(self, loader):
        '''
        Override the default loader - allows the searh to be co-opted by
        tests or maybe other searches to use the logic with a different
        data source
        
        If not set, the search will provide its own loader
        '''
        self.loader = loader

    def _load_data(self, opts):
        '''
        Load all the data needed to produce the result
        
        None is the default and is aceptable for requests that don't need to
        load any external data
        '''
        try:
            loader = self.loader
        except AttributeError:
            loader = None

        if loader:
            return loader.load(opts)

        return None

    def _process_data(self, opts, data):
        raise NotImplementedError

class UrlInterpolationProvider(RequestProvider):
    '''
    Provider that just interpolates queries into a string using %s as a placeholder
    '''
    def __init__(self, pattern):
        self.pattern = pattern

    def _process_query(self, query):
        '''
        Processing for a query before interpolating into the URL
        
        Default: don't mess with it
        '''
        return query

    def _process_data(self, opts, data):
        query = opts['query']

        query = self._process_query(query)
        url = self.pattern % query
        return request_data.PlainUrlReqData(query, url)

class InterpolatingUrlDataProvider(RequestProvider):
    '''
    Provider that downloads data from a URL with a simple url interpolation
    and then prodces results based on that data
    '''

    def __init__(self, pattern):
        self.loader = request_loader.UrlCompletionDataLoader(pattern)

    def _load_data(self, opts):
        return self.loader.load(opts['query'])

    def _process_data(self, opts, data):
        # this depends on the format of the returned data...
        raise NotImplementedError

class SimpleUrlDataCompletion(InterpolatingUrlDataProvider):
    '''
    Basic completion engine that downloads data from a URL and processes it
    into completions
    
    Optionally, it can apply another search to each completion to generate
    search urls for each one - you can do thois yourself or not at all if you
    don't want to.
    '''

    def __init__(self, url, *args, **kwargs):
        super(SimpleUrlDataCompletion, self).__init__(url, *args, **kwargs)
        self.url_prov = None

    def _get_completions(self, data):
        raise NotImplementedError

    def set_url_provider(self, prov):
        self.url_prov = prov

    def _process_data(self, opts, data):
        cs = self._get_completions(data)

        # if we can, generate the urls for the completions using the
        # provided provider
        if self.url_prov:
            for c in cs:
                c.url = self.url_prov.execute_request({'query': c.keyword}).getData()['uri']

        return request_data.CompletionReqData(cs)
