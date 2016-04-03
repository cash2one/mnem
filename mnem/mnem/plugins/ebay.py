#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory
from urllib.parse import quote, unquote
import json

class EbaySearch(mnemory.SearchMnemory):

    key = "com.ebay.search"
    defaultAlias = "ebay"

    def __init__(self, locale):
        mnemory.SearchMnemory.__init__(self, locale)

        self.base = "http://ebay." + self.tldForLocale(self.locale)

    def availableCompletions(self):
        return ["default"]

    def getRequestUrl(self, q):
        return self.base + "/sch/i.html?_nkw=%s" % quote(q)

    def defaultCompletionLoader(self, completion):

        if self.locale == "uk":
            sid = '3'
        else:
            sid = '0'

        url = "http://autosug.ebaystatic.com/autosug?kwd=%s&sId=" + sid

        return mnemory.UrlCompletionDataLoader(url)

    def getCompletions(self, result):

        result = self.stripJsonp(result)
        result = json.loads(result)

        return [mnemory.CompletionResult(c) for c in result['res']['sug']]

class Ebay(mnemory.MnemPlugin):

    def getName(self):
        return "Ebay Searches"

    def reportMnemories(self):
        return [
            EbaySearch
        ]
