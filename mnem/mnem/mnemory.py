from yapsy.IPlugin import IPlugin

from mnem import completion

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

        Mnemory.__init__(self, locale)

    def defaultLocale(self):
        '''
        None means there is no preferred locale (or the mnemory doesn't
        have a locale
        '''
        return None

    @staticmethod
    def tldForLocale(locale):
        try:
            tld = {
                'uk': 'co.uk',
                'fr': 'fr'
            }[locale]
        except KeyError:
            tld = 'com'

        return tld

    @staticmethod
    def langForLocale(locale):
        try:
            tld = {
                'uk': 'en',
                'fr': 'fr'
            }[locale]
        except KeyError:
            tld = 'en'

        return tld

    @staticmethod
    def domainForLocale(locale):

        try:
            domain = {
                'uk': "uk",
                'jp': "jp",
                'aus': "au",
            }[locale]
        except KeyError:
            domain = "us"

        return domain

    @staticmethod
    def stringLongestBetween(s, l, r, keepEnds):
        start, e = s.find(l), s.rfind(r)

        if (keepEnds):
            e = e + len(r)
        else:
            start = start + len(l)
        return s[start: e]

    @staticmethod
    def stripJsonp(jsonp):
        return SearchMnemory.stringLongestBetween(jsonp, "(", ")", False)

    def availableCompletions(self):
        """Return a list of available completion keys.
        """
        # default: doesn't provide any completions
        return []

    def availableRequests(self):
        '''
        Returns a list of requests
        Default is to provide a single default request type (since it's
        normal for a search engine to provide searches)
        
        If you override, the first item in this list is the default one for 
        this engine
        '''
        return [self.R_DEF_SEARCH]

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
        if not search_loader:
            search_loader = self._getSearchLoader(req_type)

        # load if needed TODO provide a null loader?
        if search_loader:

            try:
                data = search_loader.load(options['query'])
            except RequestLoaderNullRequest:
                return None
        else:
            data = None

        return self._getRequestData(req_type, options, data)

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

    def _getSearchLoader(self, req_type):
        '''
        Gets the default loader for the given search type
        
        Returns none if the request doesn't need to load data (eg a simple
        string interpolator) - this is default
        '''
        return None

from mnem import request_data
from urllib.parse import quote

def getSimpleUrlData(url_pat, query):
    url = url_pat % quote(query)
    return request_data.PlainUrlReqData(query, url)

def getSimpleUrlDataQuoted(opts, url_pat, key='query'):

    try:
        q = opts['query']
    except KeyError:
        raise KeyError

    return getSimpleUrlData(url_pat, q)
