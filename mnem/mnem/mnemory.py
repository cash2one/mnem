from yapsy.IPlugin import IPlugin

from mnem import completion

class MnemPlugin(IPlugin):

    def get_name(self):
        raise NotImplementedError


class SearchResult:
    pass


class UrlResult(SearchResult):

    def __init__(self, keyword, uri):
        self.uri = uri
        self.keyword = keyword

    def __str__(self):
        return self.uri


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


class Mnemory:

    defaultAlias = ""

    def __init__(self, locale=None):
        self.locale = locale

class SearchMnemory(Mnemory):

    def __init__(self, locale=None):

        # some engines have a default locale (or don't have any locale!)
        if not locale:
            locale = self.defaultLocale()

        # default completion function is none, wich will do the
        # engine's default completion action (eg load from url)
        self.compl_loader = None

        Mnemory.__init__(self, locale)

    # None means there is no preferred locale (or the mnemory doesn't
    # have a locale
    def defaultLocale(self):
        return None

    def setCompletionLoader(self, new_compl_loader):
        """
        Sets an alternative completion loader. Can be used for 
        testing, or subbing out with another engine's completion function.
        """
        self.compl_loader = new_compl_loader

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

    def load_from_url(self, url_pattern, query):

        # dprecated
        raise NotImplementedError

    def submitForSuggestions(self, completion, query):

        if not completion:
            completion = self.getDefaultCompletion()

        if (not self.providesCompletions() or
                completion not in self.availableCompletions()):
            raise completion.CompletionNotAvailableError(completion)

        # occasionally, completions for certain queries might be impossible
        # and we might be abl to catch them early rather than waiting for a
        # query to fail
        if not self.providesCompletionsForQuery(query, completion):
            return []

        # get the loader to use (default unless overriden)
        if self.compl_loader:
            loader = self.compl_loader
        else:
            loader = self.defaultCompletionLoader(completion)

        data = loader._load(query)

        compl = self.getCompletions(data)

        for c in compl:
            if not c.url:
                c.url = self.getRequestUrl(c.keyword)

        return compl

    def defaultCompletionLoader(self, completion):
        # define this in the inheritor
        raise NotImplementedError

    def providesCompletionsForQuery(self, query, completion):
        # default case is always make the call for completions
        return True

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
        return ['default']

    def providesCompletions(self):
        return len(self.availableCompletions())

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

    def getRequestData(self, req_type, options):
        '''
        Gets the request loader for this engine of the given type, with
        the given options. Normally options is a dictionary, probably with
        a 'query' value at least
        '''
        raise NotImplementedError

    def getDefaultRequestType(self):
        '''
        Returns the default request type for this engine, or None if
        no searches available
        '''
        try:
            return self.availableRequests()[0]
        except IndexError:
            return None

    def getCompletions(self, loader, completion, query):
        """Gets the results for a a given completion on this engine
        """
        # shouldn't get here if the calling code if checking
        # for validity first!
        raise NotImplementedError
