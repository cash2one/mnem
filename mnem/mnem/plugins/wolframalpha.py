#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory

from urllib.parse import quote
from json import loads


class WolframAlphaSearch(mnemory.SearchMnemory):

    key = "com.wolframalpha.search"
    defaultAlias = "wolframalpha"

    base = "http://wolframalpha.com"

    def __init__(self, locale=None):
        mnemory.SearchMnemory.__init__(self, None)

    def availableCompletions(self):
        return ["default"]

    def getRequestUrl(self, q):
        return self.base + "/input/?i=" + quote(q)

    def defaultCompletionLoader(self, completion):

        url = self.base + "/input/autocomplete.jsp?qr=0&i=%s"
        return mnemory.UrlCompletionDataLoader(url)

    def getCompletions(self, result):

        result = loads(result)

        return [mnemory.CompletionResult(c['input']) for c in result['results']]

class WolframAlpha(mnemory.MnemPlugin):

    def get_name(self):
        return "Wolfram Alpha Searches"

    def report_mnemories(self):
        return [
            WolframAlphaSearch
        ]
