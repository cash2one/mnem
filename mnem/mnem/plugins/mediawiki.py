#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory, request_provider

from json import loads

class _Completion(request_provider.SimpleUrlDataCompletion):

    def __init__(self, url):
        super(_Completion, self).__init__(url)

    def _get_completions(self, data):

        data = loads(data)

        cs = [mnemory.CompletionResult(x) for x in data[1]]
        return cs

class _Search(request_provider.UrlInterpolationProvider):

    def _process_query(self, query):
        return query.replace(" ", "_")

class MediaWikiMnemory(mnemory.SearchMnemory):

    def __init__(self, wikibase, loc=None):
        mnemory.SearchMnemory.__init__(self, loc)

        if self.locale:
            self.base = "http://%s.%s" % (self.locale, wikibase)
        else:
            self.base = "http://%s" % (wikibase)

        comp_pat = self.base + "/w/api.php?action=opensearch&format=json&search=%s"
        search_url = self.base + "/wiki/%s";

        search = _Search(search_url)
        comp = _Completion(comp_pat)

        self._add_basic_search_complete(search, comp)

    def defaultLocale(self):
        return "en"

    def getBaseUrl(self):
        return self.base

class WikipediaSearch(MediaWikiMnemory):

    key = "org.wikipedia.search"
    defaultAlias = "wikipedia"

    def __init__(self, locale):
        wikibase = "wikipedia.org"
        MediaWikiMnemory.__init__(self, wikibase, locale)

class WikisourceSearch(MediaWikiMnemory):

    key = "org.wikisource.search"
    defaultAlias = "wikisource"

    def __init__(self, locale):
        wikibase = "wikisource.org"
        MediaWikiMnemory.__init__(self, wikibase, locale)

class WikispeciesSearch(MediaWikiMnemory):

    key = "org.wikispecies.search"
    defaultAlias = "wikispecies"

    def defaultLocale(self):
        return None

    def __init__(self, locale):
        wikibase = "wikispecies.org"
        MediaWikiMnemory.__init__(self, wikibase)

class WiktionarySearch(MediaWikiMnemory):

    key = "org.wiktionary.search"
    defaultAlias = "wiktionary"

    def __init__(self, locale):
        wikibase = "wiktionary.org"
        MediaWikiMnemory.__init__(self, wikibase, locale)

class WikiquoteSearch(MediaWikiMnemory):

    key = "org.wikiquote.search"
    defaultAlias = "wikiquote"

    def __init__(self, locale):
        wikibase = "wikiquote.org"
        MediaWikiMnemory.__init__(self, wikibase, locale)

class WikibooksSearch(MediaWikiMnemory):

    key = "org.wikibooks.search"
    defaultAlias = "wikibooks"

    def __init__(self, locale):
        wikibase = "wikibooks.org"
        MediaWikiMnemory.__init__(self, wikibase, locale)

class WikinewsSearch(MediaWikiMnemory):

    key = "org.wikinews.search"
    defaultAlias = "wikinews"

    def __init__(self, locale):
        wikibase = "wikinews.org"
        MediaWikiMnemory.__init__(self, wikibase, locale)

class WikiversitySearch(MediaWikiMnemory):

    key = "org.wikiversity.search"
    defaultAlias = "wikiversity"

    def __init__(self, locale):
        wikibase = "wikiversity.org"
        MediaWikiMnemory.__init__(self, wikibase, locale)

class WikivoyageSearch(MediaWikiMnemory):

    key = "org.wikivoyage.search"
    defaultAlias = "wikivoyage"

    def __init__(self, locale):
        wikibase = "wikivoyage.org"
        MediaWikiMnemory.__init__(self, wikibase, locale)

class WikimediaCommonsSearch(MediaWikiMnemory):

    key = "org.commons.wikimedia.search"
    defaultAlias = "commons"

    def defaultLocale(self):
        return None

    def __init__(self, locale):
        wikibase = "commons.wikimedia.org"
        MediaWikiMnemory.__init__(self, wikibase)

class MediaWiki(mnemory.MnemPlugin):

    def getName(self):
        return "MediaWiki Searches"

    def reportMnemories(self):
        return [
            WikipediaSearch,
            WikisourceSearch,
            WikispeciesSearch,
            WiktionarySearch,
            WikimediaCommonsSearch,
            WikinewsSearch,
            WikibooksSearch,
            WikiversitySearch,
            WikivoyageSearch
        ]
