#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory, locale, request_provider
from json import loads

import codecs

reader = codecs.getreader("utf-8")

import html

class GoogleMnemory(mnemory.SearchMnemory):

    def defaultLocale(self):
        return "us"

class _GoogleWebCompletion(request_provider.SimpleUrlDataCompletion):

    def __init_(self, base):
        url = base + "/complete/search?client=chrome-omni&gs_ri=chrome-ext&oit=1&cp=1&pgcl=7&q=%s"
        super().__init_(url)

    def _get_completions(self, data):

        data = loads(data)
        return [mnemory.CompletionResult(x) for x in data[1]]

class GoogleSearch(GoogleMnemory):

    key = "com.google.websearch"
    defaultAlias = "google"

    def __init__(self, loc=None):
        self.base = "https://www.google." + locale.tldForLocale(loc)

        sch_pat = self.base + "/search?q=%s"

        search = request_provider.UrlInterpolationProvider(sch_pat)
        comp = _GoogleWebCompletion(self.base)

        self._add_basic_search_complete(search, comp)

        super().__init__(loc)

class _GImgComp(request_provider.SimpleUrlDataCompletion):

    def __init__(self, base, loc):
        url = base + "/complete/search?client=img&hl=%s&gs_rn=43&gs_ri=img&ds=i&cp=1&gs_id=8&q=%%s" % locale.langForLocale(loc)
        super().__init__(url)

    def _get_completions(self, data):

        def process(res):
            res = html.unescape(res.replace("<b>", "").replace("</b>", ""))
            return mnemory.CompletionResult(res)

        data = data.split("(", 1)[1][:-1]

        data = loads(data)

        return [process(x[0]) for x in data[1]]

class GoogleImageSearch(GoogleMnemory):

    key = "com.google.image"
    defaultAlias = "google-image"

    def __init__(self, loc=None):
        self.base = "https://www.google." + locale.tldForLocale(loc)

        sch_pat = self.base + "/search?tbm=isch&q=%s"

        search = request_provider.UrlInterpolationProvider(sch_pat)
        comp = _GImgComp(self.base, loc)

        self._add_basic_search_complete(search, comp)

        super().__init__(loc)

    def getBaseUrl(self):
        return self.base + "/imghp"

class _GFinComp(request_provider.SimpleUrlDataCompletion):

    def __init__(self, base):
        url = base + "/match?matchtype=matchall&q=%s"
        super().__init__(url)

    def _get_completions(self, data):

        data = loads(data)['matches']

        def parse(x):
            symbol = x['t']
            name = x['n']
            exchange = x['e']
            return mnemory.CompletionResult(symbol,
                                            description="%s - %s" % (name, exchange))

        return [parse(x) for x in data]

class GoogleFinanceSearch(GoogleMnemory):

    key = "com.google.finance"
    defaultAlias = "google-finance"

    def __init__(self, loc=None):
        self.base = "https://www.google." + locale.tldForLocale(loc) + "/finance"

        sch_pat = self.base + "?q=%s"

        search = request_provider.UrlInterpolationProvider(sch_pat)
        comp = _GFinComp(self.base)

        self._add_basic_search_complete(search, comp)

        super().__init__(loc)

    def getBaseUrl(self):
        return self.base

class _GTrendComp(request_provider.SimpleUrlDataCompletion):

    def __init__(self, base):
        url = base + "/entitiesQuery?tn=10&q=%s"
        super().__init__(url)

    def _get_completions(self, data):

        def parseResult(e):
            res = mnemory.CompletionResult(e['title'],
                    category=e['type'],
                    url=self.getRequestUrl(e['mid']))
            return res

        data = loads(data)

        try:
            res = [parseResult(x) for x in data['entityList']]
        except Exception as e:
            raise request_provider.RequestDataParseError(self, data, e)

        return res

class GoogleTrendsSearch(GoogleMnemory):

    key = "com.google.trends"
    defaultAlias = "google-trends"

    def __init__(self, loc=None):
        self.base = "https://www.google." + locale.tldForLocale(loc) + "/trends"

        sch_pat = self.base + "/explore#q=%s"

        search = request_provider.UrlInterpolationProvider(sch_pat)
        comp = _GTrendComp(self.base)

        self._add_basic_search_complete(search, comp)

        super().__init__(loc)

class GoogleScholarSearch(GoogleMnemory):

    key = "com.google.scholar"
    defaultAlias = "google-scholar"

    def __init__(self, loc=None):
        self.base = "https://www.scholar.google." + locale.tldForLocale(loc)

        sch_pat = self.base + "/scholar?q=%s"
        search = request_provider.UrlInterpolationProvider(sch_pat)

        self._add_basic_search_complete(search, None)

        super().__init__(loc)

class _YoutubeComplete(request_provider.SimpleUrlDataCompletion):

    def __init(self):
        url = "https://clients1.google.com/complete/search?client=youtube&hl=en&gl=us&gs_rn=23&gs_ri=youtube&ds=yt&cp=2&gs_id=d&q=%s"
        super().__init(url)

    def _get_completions(self, data):

        data = self.stripJsonp(data)
        result = loads(data)

        return [mnemory.CompletionResult(c[0]) for c in result[1]]

class YoutubeSearch(mnemory.SearchMnemory):

    key = "com.youtube.search"
    defaultAlias = "youtube"

    def __init__(self, loc=None):
        mnemory.SearchMnemory.__init__(self, loc)

        self.base = "http://youtube.com"

        sch_pat = self.base + "/results?search_query=%s"

        search = request_provider.UrlInterpolationProvider(sch_pat)
        comp = _YoutubeComplete()

        self._add_basic_search_complete(search, comp)

        super().__init__(loc)

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
