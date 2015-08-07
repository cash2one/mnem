#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mnemory

import json
import codecs

reader = codecs.getreader("utf-8")

from urllib.parse import quote
import html

class GoogleMnemory(mnemory.SearchMnemory):

    def defaultLocale(self):
        return "us"

    def availableCompletions(self):
        return ["default"]

class GoogleSearch(GoogleMnemory):

    key = "com.google.websearch"
    defaultAlias = "google"

    def __init__(self, locale):
        self.base = "https://www.google." + self.tldForLocale(locale)

        mnemory.SearchMnemory.__init__(self, locale)

    def getBaseUrl(self):
        return self.base

    def getRequestUrl(self, q):
        return self.base + "/search?q=%s" % quote(q)

    def getCompletions(self, completion, q):
        url = self.base + "/complete/search?client=chrome-omni&gs_ri=chrome-ext&oit=1&cp=1&pgcl=7&q=%s"

        data = self.load_from_url(url, q)
        data = data.json()

        return [mnemory.CompletionResult(x) for x in data[1]]

class GoogleImageSearch(GoogleMnemory):

    key = "com.google.image"
    defaultAlias = "google-image"

    def __init__(self, locale):
        self.base = "https://www.google." + self.tldForLocale(locale)

        mnemory.SearchMnemory.__init__(self, locale)

    def getBaseUrl(self):
        return self.base + "/imghp"

    def getRequestUrl(self, q):
        return self.base + "/search?tbm=isch&q=%s" % quote(q)

    def getCompletions(self, completion, q):

        def process(res):
            res = html.unescape(res.replace("<b>", "").replace("</b>", ""))
            return mnemory.CompletionResult(res)

        url = self.base + "/complete/search?client=img&hl=%s&gs_rn=43&gs_ri=img&ds=i&cp=1&gs_id=8&q=%%s" % self.langForLocale(self.locale)

        data = self.load_from_url(url, q).text

        data = data.split("(", 1)[1][:-1]

        data = json.loads(data)

        return [process(x[0]) for x in data[1]]

class GoogleFinanceSearch(GoogleMnemory):

    key = "com.google.finance"
    defaultAlias = "google-finance"

    def __init__(self, locale):
        self.base = "https://www.google." + self.tldForLocale(locale) + "/finance"

        mnemory.SearchMnemory.__init__(self, locale)

    def getBaseUrl(self):
        return self.base

    def getRequestUrl(self, q):
        return self.base + "?q=%s" % quote(q)

    def getCompletions(self, completion, q):

         url = self.base + "/match?matchtype=matchall&q=%s"

         data = self.load_from_url(url, q)

         data = data.json()['matches']

         def parse(x):
             symbol = x['t']
             name = x['n']
             exchange = x['e']
             return mnemory.CompletionResult(symbol, description = "%s - %s" % (name, exchange))

         return [parse(x) for x in data]

class GoogleTrendsSearch(GoogleMnemory):

    key = "com.google.trends"
    defaultAlias = "google-trends"

    def __init__(self, locale):
        self.base = "https://www.google." + self.tldForLocale(locale) + "/trends"

        mnemory.SearchMnemory.__init__(self, locale)

    def getBaseUrl(self):
        return self.base

    def getRequestUrl(self, q):
        return self.base + "/explore#q=%s" % quote(q)

    def getCompletions(self, completion, q):

        def parseResult(e):
            res = mnemory.CompletionResult(e['title'],
                    category=e['type'],
                    url=self.getRequestUrl(e['mid']))
            return res

        url = self.base + "/entitiesQuery?tn=10&q=%s"

        data = self.load_from_url(url, q).json()

        try:
            res = [parseResult(x) for x in data['entityList']]
        except Exception as e:
            raise mnemory.CompletionParseError(self, data, e)

        return res

class Google(mnemory.MnemPlugin):

    def get_name(self):
        return "Google Searches"

    def report_mnemories(self):
        return [
            GoogleSearch,
            GoogleImageSearch,
            GoogleFinanceSearch,
            GoogleTrendsSearch,
        ]
