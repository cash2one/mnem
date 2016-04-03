#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory

from json import loads

class MediaWikiMnemory(mnemory.SearchMnemory):

    def __init__(self, wikibase, locale=None):
        mnemory.SearchMnemory.__init__(self, locale)

        if self.locale:
            self.base = "http://%s.%s" % (self.locale, wikibase)
        else:
            self.base = "http://%s" % (wikibase)

    def defaultLocale(self):
        return "en"

    def availableCompletions(self):
        return ["default"]

    def getBaseUrl(self):
        return self.base

    def getRequestData(self, rtype, opts):
        return mnemory.getSimpleUrlData(self.base + "/wiki/%s",
                                        opts['query'].replace(" ", "_"))

    def defaultCompletionLoader(self, completion):
        url = self.base + "/w/api.php?action=opensearch&format=json&search=%s"
        return mnemory.completion.UrlCompletionDataLoader(url)

    def getCompletions(self, data):

        data = loads(data)

        return [mnemory.CompletionResult(x) for x in data[1]]

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
