#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory

from json import loads

class YahooSearch(mnemory.SearchMnemory):

    def __init__(self):
        mnemory.SearchMnemory.__init__(self, None)
        self.base = "https://yahoo.com"

    def availableCompletions(self):
        return ["default"]

    def getBaseUrl(self):
        return self.base


class YahooWebSearch(YahooSearch):

    key = "com.yahoo.websearch"
    defaultAlias = "yahoo"

    _completionPat = "https://search.yahoo.com/sugg/gossip/gossip-us-ura/?output=sd1&command=%s"

    def __init__(self, locale):
        YahooSearch.__init__(self)

    def getRequestData(self, rtype, opts):
        url = self.base + "/search?p=%s"
        return mnemory.getSimpleUrlDataQuoted(opts, url)

    def defaultCompletionLoader(self, completion):
        return mnemory.completion.UrlCompletionDataLoader(self._completionPat)

    def getCompletions(self, data):

        j = loads(data)

        comps = [c['k'] for c in j['r']]

        return [mnemory.CompletionResult(c) for c in comps]

class Yahoo(mnemory.MnemPlugin):

    def getName(self):
        return "Yahoo Searches"

    def reportMnemories(self):
        return [
            YahooWebSearch
        ]
