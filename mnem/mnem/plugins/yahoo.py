#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory

from json import loads

class YahooSearch(mnemory.SearchMnemory):

    def __init__(self):
        mnemory.SearchMnemory.__init__(self, None)
        self.base = "https://yahoo.com"

    def availableCompletions(self):
        return [self.R_DEF_COMPLETE]

    def getBaseUrl(self):
        return self.base


class YahooWebSearch(YahooSearch):

    key = "com.yahoo.websearch"
    defaultAlias = "yahoo"

    _completionPat = "https://search.yahoo.com/sugg/gossip/gossip-us-ura/?output=sd1&command=%s"

    def __init__(self, locale):
        YahooSearch.__init__(self)

    def _getSearchLoader(self, req_type):

        if req_type == self.R_DEF_COMPLETE:
            return mnemory.completion.UrlCompletionDataLoader(self._completionPat)

    def getRequestData(self, rtype, opts, data):
        if rtype == self.R_DEF_SEARCH:
            url = self.base + "/search?p=%s"
            return mnemory.getSimpleUrlDataQuoted(opts, url)
        else:
            return self._getCompletions(data)

    def _getCompletions(self, data):

        j = loads(data)

        comps = [c['k'] for c in j['r']]

        cs = [mnemory.CompletionResult(c) for c in comps]
        return mnemory.request_data.CompletionReqData(cs)

class Yahoo(mnemory.MnemPlugin):

    def getName(self):
        return "Yahoo Searches"

    def reportMnemories(self):
        return [
            YahooWebSearch
        ]
