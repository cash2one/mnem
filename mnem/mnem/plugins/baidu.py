#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory

import json


class BaiduSearch(mnemory.SearchMnemory):

    def __init__(self):
        mnemory.SearchMnemory.__init__(self, None)
        self.base = "https://baidu.com"

    def availableCompletions(self):
        return [self.R_DEF_COMPLETE]

    def _getSearchLoader(self, req_type):
        if req_type == self.R_DEF_COMPLETE:
            return mnemory.completion.UrlCompletionDataLoader(self._completionPat)

    def getBaseUrl(self):
        return self.base


class BaiduWebSearch(BaiduSearch):

    key = "com.baidu.websearch"
    defaultAlias = "baidu"

    _completionPat = "http://suggestion.baidu.com/su?wd=%s&json=1"

    def __init__(self, locale=None):
        BaiduSearch.__init__(self)

    def _getRequestData(self, rtype, opts, data):

        if rtype == self.R_DEF_SEARCH:
            url = self.base + "/s?wd=%s"
            return mnemory.getSimpleUrlDataQuoted(opts, url)
        else:
            return self._getCompletions(data)

    def _getCompletions(self, result):

        result = self.stripJsonp(result)

        t = json.loads(result)

        cs = [mnemory.CompletionResult(c) for c in t['s']]

        return mnemory.request_data.CompletionReqData(cs)


class BaiduImageSearch(BaiduSearch):

    key = "com.baidu.imagesearch"
    defaultAlias = "baidu-image"

    _completionPat = "http://nssug.baidu.com/su?wd=%s&prod=image"

    def __init__(self, locale=None):
        BaiduSearch.__init__(self)

    def _getRequestData(self, rtype, opts, data):

        if rtype == self.R_DEF_SEARCH:
            url = "http://image.baidu.com/search/index?tn=baiduimage&word=%s"
            return mnemory.getSimpleUrlDataQuoted(opts, url)
        else:
            return self._getCompletions(data)

    def _getCompletions(self, result):

        # ugh, no quotes in the "JSON", jsut load the array
        result = self.stringLongestBetween(result, "[", "]", True)
        result = json.loads(result)

        cs = [mnemory.CompletionResult(c) for c in result]

        return mnemory.request_data.CompletionReqData(cs)


class Baidu(mnemory.MnemPlugin):

    def getName(self):
        return "Baidu Searches"

    def reportMnemories(self):
        return [
            BaiduWebSearch,
            BaiduImageSearch
        ]
