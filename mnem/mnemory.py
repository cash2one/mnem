
from yapsy.IPlugin import IPlugin

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

    def __init__(self, orig_query):
        self.orig_query = orig_query

    def __str__(self):
        return self.orig_query

class Mnemory:

    def __init__(self, locale=None):
        self.locale = locale


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

    def submitForSuggestions(self, part):
        return self.getCompletions(part)

    def getRequestUrl(self, query):
        raise NotImplementedError

    def providesCompletions(self):
        return false;

    def getCompletions(self, query):
        raise NotImplementedError


