from yapsy.IPlugin import IPlugin

from mnem import completion, request_data

class MnemPlugin(IPlugin):

    def getName(self):
        raise NotImplementedError


class SearchResult:
    pass

class CompletionResult(SearchResult):

    def __init__(self, keyword, category="", description="", url="",
                 req_type=None):
        '''
        @param keyword: the keyword for this completion (eg 'catalyst' for 'cat')
        @param category: the (human-readable) category for this completion
        (for example "Products" or "Categories") if provided
        @param description: extended (human-readable) description of the
        completion if provided
        @param url: url of that completion's request, if provided (could
        also re-call the engine to get the same or different request URL)
        @param req_type: the type of engine request that this completion
        relates to. Default is None, which means the default search for the
        engine, if it exists.
        '''
        self.keyword = keyword
        self.description = description
        self.category = category
        self.url = url
        self.req_type = req_type

    def __str__(self):
        s = u"%s" % (self.keyword)

        if self.category:
            s += " (%s)" % self.category
        return s

class RequestLoaderNullRequest(Exception):
    '''
    Exception raised when a request loader reports that it can't proceed with
    the request due to some problem it detects with the query.
    '''

    def __init__(self, failing_query):
        self.failing_query = failing_query

    def __str__(self):
        return self.failing_query

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
        self.loader = completion.UrlCompletionDataLoader(pattern)

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

class Mnemory:

    defaultAlias = ""

    def __init__(self, locale=None):
        self.locale = locale

class SearchMnemory(Mnemory):

    R_DEF_COMPLETE = 'complete'  # useful as the default/only completion search type if an engine has one
    R_DEF_SEARCH = 'search'  # useful if the search as only one or a default search (as opposed to completion)

    def __init__(self, locale=None):

        # some engines have a default locale (or don't have any locale!)
        if not locale:
            locale = self.defaultLocale()

        self.loaders = {}

        Mnemory.__init__(self, locale)

    def defaultLocale(self):
        '''
        None means there is no preferred locale (or the mnemory doesn't
        have a locale
        '''
        return None

    def availableRequests(self):
        '''
        Returns a list of request type keys
        
        Default is to return all keys in a dict called providers, but you
        can do this yourself if you have more complex logic
        
        If you override, the first item in this list is the default one for 
        this engine
        '''
        return [p for p in self.providers]

    def availableCompletions(self):
        """
        Return a list of available completion keys. If there is a default-looking
        completion provided, the default impl will provide it
        """
        comps = []

        if self.R_DEF_COMPLETE in self.providers:
            comps.append(self.R_DEF_COMPLETE)

        return comps

    def getDefaultCompletion(self):
        """Returns the fairst available completion available
        from this search engine
        """

        comps = self.availableCompletions()

        try:
            # default is the first provided completion from
            # availableCompletions
            return comps[0]
        except IndexError:
            # hmm, should this be a separate error type?
            raise completion.CompletionNotAvailableError("$default")

    def getRequestData(self, req_type, options, search_loader=None):
        '''
        Gets the request data for this engine of the given type, with
        the given options. Normally options is a dictionary, probably with
        a 'query' value at least
        '''

        provider = self._get_provider(req_type, options)

        if search_loader:
            provider.set_loader(search_loader)

        return provider.execute_request(options)

    def _get_provider(self, req_type, opts):
        '''
        Gets the provider for a particular query type.
        
        Default is to look in a dictionary called self.providers, but you can
        implement a different method if you like
        '''

        return self.providers[req_type]

    def getDefaultRequestType(self):
        '''
        Returns the default request type for this engine, or None if
        no searches available
        '''
        try:
            return self.availableRequests()[0]
        except IndexError:
            pass

        return None

    def _add_basic_search_complete(self, search_prov, comp_prov):
        '''
        Inits self.providers with a basic URL search and a completer, with the
        completer using the search for url generation if provided
        
        This is a very common basic set of searches, and can be added to, or
        can just be ommitted if they dont apply
        '''

        self.providers = {}

        if search_prov:
            self.providers[self.R_DEF_SEARCH] = search_prov

        if comp_prov:

            if search_prov:
                comp_prov.set_url_provider(search_prov)

            self.providers[self.R_DEF_COMPLETE] = comp_prov
