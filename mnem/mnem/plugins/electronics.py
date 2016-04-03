#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory, completion

from json import loads

class OctopartSearch(mnemory.SearchMnemory):

    key = "com.octopart.search"
    defaultAlias = "octopart"

    base = "https://octopart.com"

    def __init__(self, locale=None):
        mnemory.SearchMnemory.__init__(self, None)

    def availableCompletions(self):
        return [self.R_DEF_COMPLETE]

    def _getSearchLoader(self, req_type):

        if req_type == self.R_DEF_COMPLETE:
            apikey = "6911d9b3"  # FIXME this presumably rotates...
            url = "https://octopart.com/api/v3/suggest?apikey=" + apikey + "&q=%s&grouped=true"

            return completion.UrlCompletionDataLoader(url)

    def _getRequestData(self, rtype, opts, data):

        if rtype == self.R_DEF_SEARCH:
            url = self.base + "/search?q=%s"
            return mnemory.getSimpleUrlDataQuoted(opts, url)
        else:
            return self._getCompletions(data)

    def _getCompletions(self, result):

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

        result = loads(result)

        c = [];

        for group in result['group_order']:
            c.extend(parse(group, result['results'][group]))

        return mnemory.request_data.CompletionReqData(c)

class MouserSearch(mnemory.SearchMnemory):

    key = "com.mouser.search"
    defaultAlias = "mouser"

    def __init__(self, locale):
        mnemory.SearchMnemory.__init__(self, None)

    def availableCompletions(self):
        return [self.R_DEF_COMPLETE]

    def getBaseUrl(self):
        return "http://" + self.domainForLocale(self.locale) + ".mouser.com"

    def _getSearchLoader(self, req_type):

        if req_type == self.R_DEF_COMPLETE:
            api = self.getBaseUrl() + "/ajax/autosuggestion.ashx?q=%s"
            return completion.UrlCompletionDataLoader(api)

    def _getRequestData(self, rtype, opts, data):

        if rtype == self.R_DEF_SEARCH:
            url = self.getBaseUrl() + "/Search/Refine.aspx?Keyword=%s"
            return mnemory.getSimpleUrlDataQuoted(opts, url)
        else:
            return self._getCompletions(data)

    def _getCompletions(self, data):

        def parse(entry):

            kwd, uid = entry['value'].split("##", 1)

            return mnemory.CompletionResult(kwd.strip(), url=uidUrl % uid)

        uidUrl = self.getBaseUrl() + "/Search/Refine.aspx?N=%s"

        data = loads(data)

        cs = [parse(e) for e in data]
        return mnemory.request_data.CompletionReqData(cs)


class ElectronicsSupply(mnemory.MnemPlugin):

    def getName(self):
        return "Electronics Supply Searches"

    def reportMnemories(self):
        return [
            OctopartSearch,
            MouserSearch
        ]
