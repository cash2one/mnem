#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory

from json import loads

class AmazonSearch(mnemory.SearchMnemory):

    key = "com.amazon.search"
    defaultAlias = "amazon"

    def __init__(self, locale):
        mnemory.SearchMnemory.__init__(self, locale)

        if self.locale:
            self.base = "amazon." + self.tldForLocale(self.locale)

    def defaultLocale(self):
        return "uk"

    def availableCompletions(self):
        return [self.R_DEF_COMPLETE]

    def _getSearchLoader(self, req_type):

        if req_type == self.R_DEF_COMPLETE:
            mkts = {
                'uk' : '3'
            }

            mkt = mkts[self.locale] if self.locale in mkts else '1'

            url = "https://completion." + self.base + "/search/complete?method=completion&search-alias=aps&client=amazon-search-ui&mkt=" + mkt + "&q=%s"

            return mnemory.completion.UrlCompletionDataLoader(url)

        return None

    def _getRequestData(self, rtype, opts, data):

        if rtype == self.R_DEF_SEARCH:
            url = "http://" + self.base + "/s/?field-keywords=%s"
            return mnemory.getSimpleUrlDataQuoted(opts, url)
        else:
            return self._getCompletions(data)

    def _getCompletions(self, data):
        data = loads(data)

        # the basic completions - not the "node" results
        simple_compls = data[1]

        compls = [mnemory.CompletionResult(x) for x in simple_compls]

        cs = mnemory.request_data.CompletionReqData(compls)

        return cs

class Amazon(mnemory.MnemPlugin):

    def getName(self):
        return "Amazon Searches"

    def reportMnemories(self):
        return [
            AmazonSearch
        ]
