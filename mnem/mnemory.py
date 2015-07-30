from yapsy.IPlugin import IPlugin

import requests

import urllib.request
from urllib.parse import quote

import traceback

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

class CompletionError(Exception):

    pass

class CompletionFetchError(CompletionError):

    def __init__(self, engine, url, query):
        self.engine = engine
        self.url = url
        self.query = query

    def __str__(self):
        return "%s\n%s\n%s" % (self.engine, self.url, self.query)

class CompletionParseError(CompletionError):

    def __init__(self, engine, data, innerExcept):
        self.data = data
        self.engine = engine
        self.innerExcept = innerExcept

    def __str__(self):
        return "%s\n%s\n%s" % (self.engine, self.data, self.innerExcept)

class SearchMnemory(Mnemory):

    def __init__(self, locale=None):

        # some engines have a default locale (or don't have any locale!)
        if not locale:
            locale = self.defaultLocale()

        Mnemory.__init__(self, locale)

    # None means there is no preferred locale (or the mnemory doesn't
    # have a locale
    def defaultLocale(self):
        return None

    def availableCompletions(self):
        return []

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

    def getSearchForQuery(self, query):
        url = self.getRequestUrl(query)
        return UrlResult(url)

    def load_from_url(self, url_pattern, query):

        try:
            data = requests.get(url_pattern % quote(query))
        except urllib.request.HTTPError:
            raise CompletionFetchError(self, url_pattern, query)
        finally:
            data.close()

        return data

    def submitForSuggestions(self, completion, part):

        try:
            return self.getCompletions(completion, part)
        except CompletionError as e:
            print(e)

    def getRequestUrl(self, query):
        raise NotImplementedError

    def providesCompletions(self):
        return false;

    def getCompletions(self, query):
        raise NotImplementedError


