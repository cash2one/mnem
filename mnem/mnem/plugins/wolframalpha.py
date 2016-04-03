#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory

from json import loads


class WolframAlphaSearch(mnemory.SearchMnemory):

    key = "com.wolframalpha.search"
    defaultAlias = "wolframalpha"

    base = "http://wolframalpha.com"

    def __init__(self, locale=None):
        mnemory.SearchMnemory.__init__(self, None)

    def availableCompletions(self):
        return [self.R_DEF_COMPLETE]

    def _getSearchLoader(self, req_type):

        if req_type == self.R_DEF_COMPLETE:
            url = self.base + "/input/autocomplete.jsp?qr=0&i=%s"
            return mnemory.completion.UrlCompletionDataLoader(url)

    def _getRequestData(self, rtype, opts, data):
        if rtype == self.R_DEF_SEARCH:
            url = self.base + "/input/?i=%s"
            return mnemory.getSimpleUrlDataQuoted(opts, url)
        else:
            return self._getCompletions(data)

    def _getCompletions(self, result):

        result = loads(result)

        cs = [mnemory.CompletionResult(c['input']) for c in result['results']]
        return mnemory.request_data.CompletionReqData(cs)

class WolframAlpha(mnemory.MnemPlugin):

    def getName(self):
        return "Wolfram Alpha Searches"

    def reportMnemories(self):
        return [
            WolframAlphaSearch
        ]
