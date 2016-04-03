#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory

from urllib.parse import quote, unquote

class YouDaoDictSearch(mnemory.SearchMnemory):

    key = "com.youdao.dict.search"
    defaultAlias = "youdao"

    def __init__(self, locale=None):
        mnemory.SearchMnemory.__init__(self, None)

        self.base = "https://dict.youdao.com"

    def getBaseUrl(self):
        return self.base

    def availableCompletions(self):
        return [self.R_DEF_COMPLETE]

    def _getSearchLoader(self, req_type):

        if req_type == self.R_DEF_COMPLETE:
            url = "http://dsuggest.ydstatic.com/suggest/suggest.s?query=%s"
            return mnemory.completion.UrlCompletionDataLoader(url)

    def getRequestData(self, rtype, opts, data):
        if rtype == self.R_DEF_SEARCH:
            url = self.base + '/search?q=%s&keyfrom=dict.index'
            return mnemory.getSimpleUrlDataQuoted(opts, url)
        else:
            return self._getCompletions(data)

    def _getCompletions(self, data):

        cs = []

        # this is pretty ugly but it gets us the right results
        for r in data.split("this.txtBox.value%3D")[1:]:
            quoted = r.split("%22", 1)[0]
            cs.append(unquote(quoted))

        cs = [mnemory.CompletionResult(c) for c in cs]

        return mnemory.request_data.CompletionReqData(cs)

class YouDao(mnemory.MnemPlugin):

    def getName(self):
        return "YouDao Searches"

    def reportMnemories(self):
        return [
            YouDaoDictSearch
        ]
