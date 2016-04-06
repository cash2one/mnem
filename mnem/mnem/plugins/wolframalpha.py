#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory, request_provider

from json import loads

class _Completion(request_provider.SimpleUrlDataCompletion):

    def __init__(self):
        url = WolframAlphaSearch.base + "/input/autocomplete.jsp?qr=0&i=%s"
        super().__init__(url)

    def _get_completions(self, data):

        data = loads(data)

        cs = [mnemory.CompletionResult(c['input']) for c in data['results']]

        return cs

class WolframAlphaSearch(mnemory.SearchMnemory):

    key = "com.wolframalpha.search"
    defaultAlias = "wolframalpha"

    base = "http://wolframalpha.com"

    def __init__(self, loc=None):
        super().__init__(loc)

        search_url = self.base + "/input/?i=%s"

        search = request_provider.UrlInterpolationProvider(search_url)
        comp = _Completion()

        self._add_basic_search_complete(search, comp)

class WolframAlpha(mnemory.MnemPlugin):

    def getName(self):
        return "Wolfram Alpha Searches"

    def reportMnemories(self):
        return [
            WolframAlphaSearch
        ]
