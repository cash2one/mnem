#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mnemory
from urllib.parse import quote, unquote
import json


class WolframAlphaSearch(mnemory.SearchMnemory):

    key = "com.wolframalpha.search"
    defaultAlias = "wolframalpha"

    base = "http://wolframalpha.com"

    def __init__(self, locale):
        mnemory.SearchMnemory.__init__(self, None)

    def getRequestUrl(self, q):
        return self.base + "/input/?i=" + quote(q)

    def getCompletions(self, completion, q):

        url = self.base + "/input/autocomplete.jsp?qr=0&i=%s"
        result = self.load_from_url(url, q).json()

        return [mnemory.CompletionResult(c['input']) for c in result['results']]

class WolframAlpha(mnemory.MnemPlugin):

    def get_name(self):
        return "Wolfram Alpha Searches"

    def report_mnemories(self):
        return [
            WolframAlphaSearch
        ]
