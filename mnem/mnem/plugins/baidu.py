#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory, data_utils, request_provider

import json


class BaiduSearch(mnemory.SearchMnemory):

    def __init__(self):
        mnemory.SearchMnemory.__init__(self, None)
        self.base = "https://baidu.com"

    def getBaseUrl(self):
        return self.base

class _BdComp(request_provider.SimpleUrlDataCompletion):

    def __init__(self):
        completionPat = "http://suggestion.baidu.com/su?wd=%s&json=1"
        super().__init__(completionPat)

    def _get_completions(self, data):

        result = data_utils.stripJsonp(data)

        t = json.loads(result)

        cs = [mnemory.CompletionResult(c) for c in t['s']]
        return cs

class BaiduWebSearch(BaiduSearch):

    key = "com.baidu.websearch"
    defaultAlias = "baidu"

    def __init__(self, locale=None):
        super().__init__()

        s_url = self.base + "/s?wd=%s"

        search = request_provider.UrlInterpolationProvider(s_url)
        comp = _BdComp()

        self._add_basic_search_complete(search, comp)

class _BdProductComp(request_provider.SimpleUrlDataCompletion):

    def __init__(self, prod):
        pat = "http://nssug.baidu.com/su?wd=%%s&prod=%s" % prod
        super().__init__(pat)

    def _get_completions(self, data):

        # ugh, no quotes in the "JSON", just load the array
        result = data_utils.stringLongestBetween(data, "[", "]", True)
        result = json.loads(result)

        cs = [mnemory.CompletionResult(c) for c in result]
        return cs

class BaiduImageSearch(BaiduSearch):

    key = "com.baidu.imagesearch"
    defaultAlias = "baidu-image"

    def __init__(self, locale=None):
        super().__init__()

        s_url = "http://image.baidu.com/search/index?tn=baiduimage&word=%s"

        search = request_provider.UrlInterpolationProvider(s_url)
        comp = _BdProductComp('image')

        self._add_basic_search_complete(search, comp)

class BaiduWenkuSearch(BaiduSearch):

    key = "com.baidu.wenku"
    defaultAlias = "baidu-wenku"

    def __init__(self, locale=None):
        super().__init__()

        s_url = "http://wenku.baidu.com/search?word=%s"

        search = request_provider.UrlInterpolationProvider(s_url)
        comp = _BdProductComp('wenku')

        self._add_basic_search_complete(search, comp)

class Baidu(mnemory.MnemPlugin):

    def getName(self):
        return "Baidu Searches"

    def reportMnemories(self):
        return [
            BaiduWebSearch,
            BaiduImageSearch,
            BaiduWenkuSearch
        ]
