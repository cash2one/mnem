#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory

from urllib.parse import quote
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

    def getRequestUrl(self, q):
        return self.base + "/search?p=%s" % quote(q)

    def defaultCompletionLoader(self, completion):
        return mnemory.UrlCompletionDataLoader(self._completionPat)

    def getCompletions(self, data):

        j = loads(data)

        comps = [c['k'] for c in j['r']]

        return [mnemory.CompletionResult(c) for c in comps]

class Yahoo(mnemory.MnemPlugin):

    def get_name(self):
        return "Yahoo Searches"

    def report_mnemories(self):
        return [
            YahooWebSearch
        ]
