from yapsy.IPlugin import IPlugin

import requests

import urllib.request
from urllib.parse import quote

from mnem.mnem import MnemError


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

    def __init__(self, keyword, category="", description="", url=""):
        self.keyword = keyword
        self.description = description
        self.category = category
        self.url = url

    def __str__(self):
        s = u"%s" % (self.keyword)

        if self.category:
            s += " (%s)" % self.category
        return s


class Mnemory:

    defaultAlias = ""

    def __init__(self, locale=None):
        self.locale = locale


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

    def getSearchForQuery(self, query):
        url = self.getRequestUrl(query)
        return UrlResult(query, url)

    def load_from_url(self, url_pattern, query):

        # dprecated
        raise NotImplementedError

    def submitForSuggestions(self, completion, query):

        if not completion:
            completion = self.getDefaultCompletion()

        if (not self.providesCompletions() or
                completion not in self.availableCompletions()):
            raise CompletionNotAvailableError(completion)

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

    def availableCompletions(self):
        """Return a list of available completion keys.
        """
        # default: doesn't provide any completions
        return []

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
            raise CompletionNotAvailableError("$default")

    def getRequestUrl(self, query):
        """Gets the URL for a search query
        """
        raise NotImplementedError

    def getCompletions(self, loader, completion, query):
        """Gets the results for a a given completion on this engine
        """
        # shouldn't get here if the calling code if checking
        # for validity first!
        raise NotImplementedError
