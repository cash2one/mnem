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

    def getRequestData(self, rtype, opts):
        url = self.base + "/input/?i=%s"
        return mnemory.getSimpleUrlDataQuoted(opts, url)

    def defaultCompletionLoader(self, completion):

        url = self.base + "/input/autocomplete.jsp?qr=0&i=%s"
        return mnemory.completion.UrlCompletionDataLoader(url)

    def getCompletions(self, result):

        result = loads(result)

        return [mnemory.CompletionResult(c['input']) for c in result['results']]

class WolframAlpha(mnemory.MnemPlugin):

    def getName(self):
        return "Wolfram Alpha Searches"

    def reportMnemories(self):
        return [
            WolframAlphaSearch
        ]
