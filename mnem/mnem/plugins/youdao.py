#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory

from urllib.parse import unquote

class _Completion(mnemory.SimpleUrlDataCompletion):

    def __init__(self):
        url = "http://dsuggest.ydstatic.com/suggest/suggest.s?query=%s"
        super(_Completion, self).__init__(url)

    def _get_completions(self, data):

        cs = []

        # this is pretty ugly but it gets us the right results
        for r in data.split("this.txtBox.value%3D")[1:]:
            quoted = r.split("%22", 1)[0]
            kw = unquote(quoted)
            cs.append(kw)

        cs = [mnemory.CompletionResult(c) for c in cs]
        return cs

class YouDaoDictSearch(mnemory.SearchMnemory):

    key = "com.youdao.dict.search"
    defaultAlias = "youdao"

    def __init__(self, locale=None):
        mnemory.SearchMnemory.__init__(self, None)

        self.base = "https://dict.youdao.com"

        search_url = self.base + '/search?q=%s&keyfrom=dict.index'

        search = mnemory.UrlInterpolationProvider(search_url)
        comp = _Completion()

        self._add_basic_search_complete(search, comp)

    def getBaseUrl(self):
        return self.base

class YouDao(mnemory.MnemPlugin):

    def getName(self):
        return "YouDao Searches"

    def reportMnemories(self):
        return [
            YouDaoDictSearch
        ]
