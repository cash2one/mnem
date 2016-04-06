#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory, locale, data_utils
import json

class _Complete(mnemory.SimpleUrlDataCompletion):

    def __init__(self, loc):
        if loc == "uk":
            sid = '3'
        else:
            sid = '0'

        url = "http://autosug.ebaystatic.com/autosug?kwd=%s&sId=" + sid

        super().__init__(url)

    def _get_completions(self, result):

        result = data_utils.stripJsonp(result)
        result = json.loads(result)

        cs = [mnemory.CompletionResult(c) for c in result['res']['sug']]

        return cs

class EbaySearch(mnemory.SearchMnemory):

    key = "com.ebay.search"
    defaultAlias = "ebay"

    def __init__(self, loc):
        mnemory.SearchMnemory.__init__(self, loc)

        self.base = "http://ebay." + locale.tldForLocale(loc)

        search_url = self.base + "/sch/i.html?_nkw=%s"

        search = mnemory.UrlInterpolationProvider(search_url)
        comp = _Complete(loc)

        self._add_basic_search_complete(search, comp)

class Ebay(mnemory.MnemPlugin):

    def getName(self):
        return "Ebay Searches"

    def reportMnemories(self):
        return [
            EbaySearch
        ]
