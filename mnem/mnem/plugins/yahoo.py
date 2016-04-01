#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory

from urllib.parse import quote
from lxml.etree import fromstring


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

    _completionPat = "https://search.yahoo.com/sugg/gossip/gossip-us-ura/?pq=%s"

    def __init__(self, locale):
        YahooSearch.__init__(self)

    def getRequestUrl(self, q):
        return self.base + "/search?p=%s" % quote(q)

    def getCompletions(self, completion, q):

        result = self.load_from_url(self._completionPat, q).text

        x = fromstring(result)

        comps = [s.attrib['k'] for s in x if s.tag == 's']

        return [mnemory.CompletionResult(c) for c in comps]

class Yahoo(mnemory.MnemPlugin):

    def get_name(self):
        return "Yahoo Searches"

    def report_mnemories(self):
        return [
            YahooWebSearch
        ]
