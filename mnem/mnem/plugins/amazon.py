#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory

from json import loads
from urllib.parse import quote

class AmazonSearch(mnemory.SearchMnemory):

    key = "com.amazon.search"
    defaultAlias = "amazon"

    def __init__(self, locale):
        mnemory.SearchMnemory.__init__(self, locale)

        if self.locale:
            self.base = "amazon." + self.tldForLocale(self.locale)

    def defaultLocale(self):
        return "uk"

    def availableCompletions(self):
        return ["default"]

    def getBaseUrl(self):
        return self.base

    def getRequestUrl(self, q):
        return "http://" + self.base + "/s/?field-keywords=" + quote(q)

    def defaultCompletionLoader(self, completion):
        mkts = {
            'uk' : '3'
        }

        mkt = mkts[self.locale] if self.locale in mkts else '1'

        url = "https://completion." + self.base + "/search/complete?method=completion&search-alias=aps&client=amazon-search-ui&mkt=" + mkt + "&q=%s"

        return mnemory.UrlCompletionDataLoader(url)

    def getCompletions(self, data):
        data = loads(data)

        # the basic completions - not the "node" results
        simple_compls = data[1]

        compls = [mnemory.CompletionResult(x) for x in simple_compls]

        return compls

class Amazon(mnemory.MnemPlugin):

    def getName(self):
        return "Amazon Searches"

    def reportMnemories(self):
        return [
            AmazonSearch
        ]
