#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory, locale, request_provider

from json import loads

class _OctopartComp(request_provider.SimpleUrlDataCompletion):

    def __init__(self, base):
        self.base = base

        apikey = "6911d9b3"  # FIXME this presumably rotates...
        url = "https://octopart.com/api/v3/suggest?apikey=" + apikey + "&q=%s&grouped=true"

        super().__init__(url)

    def _get_completions(self, data):
        def parse(typ, cs):
            res = []
            for c in cs:
                if typ == "query":
                    url = None  # use the req url
                elif typ == "part" or typ == "brand":
                    url = self.base + c['octopart_url']
                elif typ == "category":
                    args = ["category_uids", c['uid']]

                    url = ("https://octopart.com/search?filter%5Bfields%5D%5B" +
                                args[0] + "%5D%5B%5D=" + args[1])

                res.append(mnemory.CompletionResult(c['text'], url=url, category=typ))
            return res

        result = loads(data)

        c = []

        for group in result['group_order']:
            c.extend(parse(group, result['results'][group]))

        return c

class OctopartSearch(mnemory.SearchMnemory):

    key = "com.octopart.search"
    defaultAlias = "octopart"

    base = "https://octopart.com"

    def __init__(self, locale=None):
        mnemory.SearchMnemory.__init__(self, None)

        search_url = self.base + "/search?q=%s"

        search = request_provider.UrlInterpolationProvider(search_url)
        comp = _OctopartComp(self.base)

        self._add_basic_search_complete(search, comp)

class _MouserComplete(request_provider.SimpleUrlDataCompletion):

    def __init__(self, base):
        self.base = base
        url = base + "/ajax/autosuggestion.ashx?q=%s"
        super().__init__(url)

    def _get_completions(self, data):
        def parse(entry):

            kwd, uid = entry['value'].split("##", 1)

            return mnemory.CompletionResult(kwd.strip(), url=uidUrl % uid)

        uidUrl = self.base + "/Search/Refine.aspx?N=%s"

        print(data)

        try:
            data = loads(data)
        except ValueError as e:
            raise request_provider.RequestDataParseError(self, data, e)

        cs = [parse(e) for e in data]
        return cs

class MouserSearch(mnemory.SearchMnemory):

    key = "com.mouser.search"
    defaultAlias = "mouser"

    def __init__(self, loc):
        super().__init__(loc)

        search_url = self.getBaseUrl() + "/Search/Refine.aspx?Keyword=%s"

        search = request_provider.UrlInterpolationProvider(search_url)
        comp = _MouserComplete(self.getBaseUrl())

        self._add_basic_search_complete(search, comp)

    def getBaseUrl(self):
        return "http://" + locale.domainForLocale(self.locale) + ".mouser.com"


class ElectronicsSupply(mnemory.MnemPlugin):

    def getName(self):
        return "Electronics Supply Searches"

    def reportMnemories(self):
        return [
            OctopartSearch,
            MouserSearch
        ]
