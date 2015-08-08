#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mnemory
from urllib.parse import quote, unquote
import json

class OctopartSearch(mnemory.SearchMnemory):

    key = "com.octopart.search"
    defaultAlias = "octopart"

    base = "https://octopart.com"

    def __init__(self, locale):
        mnemory.SearchMnemory.__init__(self, None)

    def getRequestUrl(self, q):
        return self.base + "/search?q=" + quote(q)

    def getCompletions(self, completion, q):

        def parse(typ, cs):
            res = []
            for c in cs:
                if typ == "query":
                    url = None #use the req url
                elif typ == "part" or typ == "brand":
                    url = self.base + c['octopart_url']
                elif typ == "category":
                    args = ["category_uids", c['uid']]

                    url = ("https://octopart.com/search?filter%5Bfields%5D%5B" +
                                args[0] + "%5D%5B%5D=" + args[1])

                res.append(mnemory.CompletionResult(c['text'], url=url, category=typ))
            return res

        apikey = "6911d9b3" # FIXME this presumably rotates...
        url = "https://octopart.com/api/v3/suggest?apikey=" + apikey + "&q=%s&grouped=true"

        result = self.load_from_url(url, q).json()

        c = [];

        for group in result['group_order']:
            c.extend(parse(group, result['results'][group]))

        return c

class ElectronicsSupply(mnemory.MnemPlugin):

    def get_name(self):
        return "Electronics Supply Searches"

    def report_mnemories(self):
        return [
            OctopartSearch
        ]
