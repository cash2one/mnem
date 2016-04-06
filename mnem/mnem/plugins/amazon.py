#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory, locale, request_provider

from json import loads

class _Completion(request_provider.SimpleUrlDataCompletion):

    def __init__(self, base, loc):

        mkts = {
            'uk' : '3'
        }

        try:
            mkt = mkts[loc]
        except KeyError:
            mkt = '1'

        url = "https://completion." + base + "/search/complete?method=completion&search-alias=aps&client=amazon-search-ui&mkt=" + mkt + "&q=%s"

        super().__init__(url)

    def _get_completions(self, data):
        data = loads(data)

        # the basic completions - not the "node" results
        simple_compls = data[1]

        compls = [mnemory.CompletionResult(x) for x in simple_compls]
        return compls

class AmazonSearch(mnemory.SearchMnemory):

    key = "com.amazon.search"
    defaultAlias = "amazon"

    def __init__(self, loc):
        mnemory.SearchMnemory.__init__(self, loc)

        self.base = "amazon." + locale.tldForLocale(self.locale)

        s_url = "http://" + self.base + "/s/?field-keywords=%s"

        search = request_provider.UrlInterpolationProvider(s_url)
        comp = _Completion(self.base, loc)

        self._add_basic_search_complete(search, comp)

    def defaultLocale(self):
        return "uk"

class Amazon(mnemory.MnemPlugin):

    def getName(self):
        return "Amazon Searches"

    def reportMnemories(self):
        return [
            AmazonSearch
        ]
