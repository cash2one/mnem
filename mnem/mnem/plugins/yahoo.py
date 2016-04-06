#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory, request_provider

from json import loads

class YahooSearch(mnemory.SearchMnemory):

    def __init__(self, locale):
        mnemory.SearchMnemory.__init__(self, locale)
        self.base = "https://yahoo.com"

    def getBaseUrl(self):
        return self.base

class _Completion(request_provider.SimpleUrlDataCompletion):

    def __init__(self):
        url = "https://search.yahoo.com/sugg/gossip/gossip-us-ura/?output=sd1&command=%s"
        super(_Completion, self).__init__(url)

    def _get_completions(self, data):

        def process(keyword):
            c = mnemory.CompletionResult(keyword)
            return c

        j = loads(data)

        comps = [c['k'] for c in j['r']]

        cs = [process(keyword) for keyword in comps]
        return cs

class YahooWebSearch(YahooSearch):

    key = "com.yahoo.websearch"
    defaultAlias = "yahoo"

    def __init__(self, locale):
        super(YahooWebSearch, self).__init__(locale)

        search = request_provider.UrlInterpolationProvider(self.base + "/search?p=%s")
        comp = _Completion()

        self._add_basic_search_complete(search, comp)

class Yahoo(mnemory.MnemPlugin):

    def getName(self):
        return "Yahoo Searches"

    def reportMnemories(self):
        return [
            YahooWebSearch
        ]
