#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory

from mnem import completion
from mnem.completion import UrlCompletionDataLoader as UCL
from json import loads

import codecs

reader = codecs.getreader("utf-8")

from urllib.parse import quote
import html

class GoogleMnemory(mnemory.SearchMnemory):

    def defaultLocale(self):
        return "us"

    def availableCompletions(self):
        # google mnemories normally provide at least one "default"
        # completion
        return ["default"]

class GoogleSearch(GoogleMnemory):

    key = "com.google.websearch"
    defaultAlias = "google"

    def __init__(self, locale):
        self.base = "https://www.google." + self.tldForLocale(locale)

        mnemory.SearchMnemory.__init__(self, locale)

    def getBaseUrl(self):
        return self.base

    def getRequestData(self, rtype, opts):
        url = self.base + "/search?q=%s"
        return mnemory.getSimpleUrlDataQuoted(opts, url)

    def defaultCompletionLoader(self, completion):
        url = self.base + "/complete/search?client=chrome-omni&gs_ri=chrome-ext&oit=1&cp=1&pgcl=7&q=%s"
        return UCL(url)

    def getCompletions(self, data):

        data = loads(data)

        return [mnemory.CompletionResult(x) for x in data[1]]

class GoogleImageSearch(GoogleMnemory):

    key = "com.google.image"
    defaultAlias = "google-image"

    def __init__(self, locale):
        self.base = "https://www.google." + self.tldForLocale(locale)

        mnemory.SearchMnemory.__init__(self, locale)

    def getBaseUrl(self):
        return self.base + "/imghp"

    def getRequestData(self, rtype, opts):
        url = self.base + "/search?tbm=isch&q=%s"
        return mnemory.getSimpleUrlDataQuoted(opts, url)

    def defaultCompletionLoader(self, completion):
        url = self.base + "/complete/search?client=img&hl=%s&gs_rn=43&gs_ri=img&ds=i&cp=1&gs_id=8&q=%%s" % self.langForLocale(self.locale)
        return UCL(url)

    def getCompletions(self, data):

        def process(res):
            res = html.unescape(res.replace("<b>", "").replace("</b>", ""))
            return mnemory.CompletionResult(res)

        data = data.split("(", 1)[1][:-1]

        data = loads(data)

        return [process(x[0]) for x in data[1]]

class GoogleFinanceSearch(GoogleMnemory):

    key = "com.google.finance"
    defaultAlias = "google-finance"

    def __init__(self, locale):
        self.base = "https://www.google." + self.tldForLocale(locale) + "/finance"

        mnemory.SearchMnemory.__init__(self, locale)

    def getBaseUrl(self):
        return self.base

    def getRequestData(self, rtype, opts):
        url = self.base + "?q=%s"
        return mnemory.getSimpleUrlDataQuoted(opts, url)

    def defaultCompletionLoader(self, completion):
        url = self.base + "/match?matchtype=matchall&q=%s"
        return UCL(url)

    def getCompletions(self, data):

        data = loads(data)['matches']

        def parse(x):
            symbol = x['t']
            name = x['n']
            exchange = x['e']
            return mnemory.CompletionResult(symbol,
                                            description="%s - %s" % (name, exchange))

        return [parse(x) for x in data]

class GoogleTrendsSearch(GoogleMnemory):

    key = "com.google.trends"
    defaultAlias = "google-trends"

    def __init__(self, locale):
        self.base = "https://www.google." + self.tldForLocale(locale) + "/trends"

        mnemory.SearchMnemory.__init__(self, locale)

    def getRequestData(self, rtype, opts):
        url = self.base + "/explore#q=%s"
        return mnemory.getSimpleUrlDataQuoted(opts, url)

    def defaultCompletionLoader(self, completion):
        url = self.base + "/entitiesQuery?tn=10&q=%s"
        return UCL(url)

    def getCompletions(self, data):

        def parseResult(e):
            res = mnemory.CompletionResult(e['title'],
                    category=e['type'],
                    url=self.getRequestUrl(e['mid']))
            return res

        data = loads(data)

        try:
            res = [parseResult(x) for x in data['entityList']]
        except Exception as e:
            raise completion.CompletionParseError(self, data, e)

        return res

class GoogleScholarSearch(GoogleMnemory):

    key = "com.google.scholar"
    defaultAlias = "google-scholar"

    def __init__(self, locale):
        self.base = "https://www.scholar.google." + self.tldForLocale(locale)

        mnemory.SearchMnemory.__init__(self, locale)

    def getRequestData(self, rtype, opts):
        url = self.base + "/scholar?q=%s"
        return mnemory.getSimpleUrlDataQuoted(opts, url)

    def availableCompletions(self):
        """Scholar doesn't have completions
        """
        return []

class YoutubeSearch(mnemory.SearchMnemory):

    key = "com.youtube.search"
    defaultAlias = "youtube"

    def __init__(self, locale):
        mnemory.SearchMnemory.__init__(self, locale)

        self.base = "http://youtube.com"

    def getRequestData(self, rtype, opts):
        url = self.base + "/results?search_query=%s"
        return mnemory.getSimpleUrlDataQuoted(opts, url)

    def defaultCompletionLoader(self, completion):
        url = "https://clients1.google.com/complete/search?client=youtube&hl=en&gl=us&gs_rn=23&gs_ri=youtube&ds=yt&cp=2&gs_id=d&q=%s"
        return UCL(url)

    def getCompletions(self, data):

        data = self.stripJsonp(data)
        result = loads(data)

        return [mnemory.CompletionResult(c[0]) for c in result[1]]

class Google(mnemory.MnemPlugin):

    def getName(self):
        return "Google Searches"

    def reportMnemories(self):
        return [
            GoogleSearch,
            GoogleImageSearch,
            GoogleFinanceSearch,
            GoogleTrendsSearch,
            GoogleScholarSearch,
            YoutubeSearch
        ]
