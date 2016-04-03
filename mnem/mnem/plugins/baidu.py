#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory

import json


class BaiduSearch(mnemory.SearchMnemory):

    def __init__(self):
        mnemory.SearchMnemory.__init__(self, None)
        self.base = "https://baidu.com"

    def availableCompletions(self):
        return ["default"]

    def getBaseUrl(self):
        return self.base


class BaiduWebSearch(BaiduSearch):

    key = "com.baidu.websearch"
    defaultAlias = "baidu"

    _completionPat = "http://suggestion.baidu.com/su?wd=%s&json=1"

    def __init__(self, locale=None):
        BaiduSearch.__init__(self)

    def getRequestData(self, rtype, opts):
        url = self.base + "/s?wd=%s"
        return mnemory.getSimpleUrlDataQuoted(opts, url)

    def getCompletions(self, result):

        result = self.stripJsonp(result)

        t = json.loads(result)

        return [mnemory.CompletionResult(c) for c in t['s']]


class BaiduImageSearch(BaiduSearch):

    key = "com.baidu.imagesearch"
    defaultAlias = "baidu-image"

    _completionPat = "http://nssug.baidu.com/su?wd=%s&prod=image"

    def __init__(self, locale=None):
        BaiduSearch.__init__(self)

    def getRequestData(self, rtype, opts):
        url = "http://image.baidu.com/search/index?tn=baiduimage&word=%s"
        return mnemory.getSimpleUrlDataQuoted(opts, url)

    def defaultCompletionLoader(self, completion):
        return mnemory.completion.UrlCompletionDataLoader(self._completionPat)

    def getCompletions(self, result):

        # ugh, no quotes in the "JSON", jsut load the array
        result = self.stringLongestBetween(result, "[", "]", True)
        result = json.loads(result)

        return [mnemory.CompletionResult(c) for c in result]


class Baidu(mnemory.MnemPlugin):

    def getName(self):
        return "Baidu Searches"

    def reportMnemories(self):
        return [
            BaiduWebSearch,
            BaiduImageSearch
        ]
