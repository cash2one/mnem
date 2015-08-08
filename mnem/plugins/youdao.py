#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mnemory

from urllib.parse import quote, unquote

class YouDaoDictSearch(mnemory.SearchMnemory):

    key = "com.youdao.dict.search"
    defaultAlias = "youdao"

    def __init__(self, locale):
        mnemory.SearchMnemory.__init__(self, None)

        self.base = "https://dict.youdao.com"

    def getBaseUrl(self):
        return self.base

    def getRequestUrl(self, q):
        return "http://dict.youdao.com/search?q=%s&keyfrom=dict.index" % quote(q)

    def getCompletions(self, completion, q):

        url = "http://dsuggest.ydstatic.com/suggest/suggest.s?query=%s"

        cs = []

        t = self.load_from_url(url, q).text

        # this is pretty ugly but it gets us the right results
        for r in t.split("this.txtBox.value%3D")[1:]:
            quoted = r.split("%22",1)[0]
            cs.append(unquote(quoted))

        return [mnemory.CompletionResult(c) for c in cs]

class YouDao(mnemory.MnemPlugin):

    def get_name(self):
        return "YouDao Searches"

    def report_mnemories(self):
        return [
            YouDaoDictSearch
        ]
