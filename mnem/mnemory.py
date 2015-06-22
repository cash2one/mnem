
from yapsy.IPlugin import IPlugin

import urllib2
from urllib import quote

class MnemPlugin(IPlugin):

    def get_name(self):
        raise NotImplementedError

class SearchResult:
    pass

class UrlResult(SearchResult):

    def __init__(self, uri):
        self.uri = uri

    def __str__(self):
        return self.uri

class CompletionResult(SearchResult):

    def __init__(self, keyword, category="", url=""):
        self.keyword = keyword

    def __str__(self):
        return "%s (%s)" % (self.keyword, self.category)

class Mnemory:

    def __init__(self, locale=None):
        self.locale = locale

class CompletionError(Exception):

    pass

class CompletionFetchError(CompletionError):

    def __init__(self, engine, url, query):
        self.engine = engine
        self.url = url
        self.query = query

    def __str__(self):
        return self.engine, self.url, self.query

class CompletionParseError(CompletionError):

    def __init__(self, engine, data, innerExcept):
        self.data = data
        self.engine = engine
        self.innerExcept = innerExcept

    def __str__(self):
        return self.engine, self.data, self.innerExcept

class SearchMnemory(Mnemory):

    def __init__(self, locale=None):
        Mnemory.__init__(self, locale)

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

    def submitSearch(self, query):
        url = self.getRequestUrl(query)
        return UrlResult(url)

    def load_from_url(self, url_pattern, query):

        try:
            data = urllib2.urlopen(url_pattern % quote(query)).read()
        except urllib.HTTPError:
            raise CompletionFetchError(self, url_pattern, query)

        return data

    def submitForSuggestions(self, part):

         return self.getCompletions(part)

    def getRequestUrl(self, query):
        raise NotImplementedError

    def providesCompletions(self):
        return false;

    def getCompletions(self, query):
        raise NotImplementedError


