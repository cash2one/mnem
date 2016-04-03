#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory
import json

class EbaySearch(mnemory.SearchMnemory):

    key = "com.ebay.search"
    defaultAlias = "ebay"

    def __init__(self, locale):
        mnemory.SearchMnemory.__init__(self, locale)

        self.base = "http://ebay." + self.tldForLocale(self.locale)

    def availableCompletions(self):
        return [self.R_DEF_COMPLETE]

    def _getSearchLoader(self, req_type):

        if req_type == self.R_DEF_COMPLETE:
            if self.locale == "uk":
                sid = '3'
            else:
                sid = '0'

            url = "http://autosug.ebaystatic.com/autosug?kwd=%s&sId=" + sid

            return mnemory.completion.UrlCompletionDataLoader(url)

    def _getRequestData(self, rtype, opts, data):

        if rtype == self.R_DEF_SEARCH:
            url = self.base + "/sch/i.html?_nkw=%s"
            return mnemory.getSimpleUrlDataQuoted(opts, url)
        else:
            return self._getCompletions(data)

    def _getCompletions(self, result):

        result = self.stripJsonp(result)
        result = json.loads(result)

        cs = [mnemory.CompletionResult(c) for c in result['res']['sug']]

        return mnemory.request_data.CompletionReqData(cs)

class Ebay(mnemory.MnemPlugin):

    def getName(self):
        return "Ebay Searches"

    def reportMnemories(self):
        return [
            EbaySearch
        ]
