#! /usr/bin/env python

import mnemory

import json

from urllib import quote
import HTMLParser

class GoogleSearch(mnemory.SearchMnemory):

    def __init__(self, locale):
        self.base = "https://www.google." + self.tldForLocale(locale)

        mnemory.SearchMnemory.__init__(self, locale)

    def getBaseUrl(self):
        return self.base

    def getRequestUrl(self, q):
        return self.base + "/search?q=%s" % quote(q)

    def getCompletions(self, q):

        url = self.base + "/complete/search?client=chrome-omni&gs_ri=chrome-ext&oit=1&cp=1&pgcl=7&q=%s"

        data = self.load_from_url(url, q)
        data = json.loads(data)

        return [mnemory.CompletionResult(x.encode('utf-8')) for x in data[1]]

class GoogleImageSearch(mnemory.SearchMnemory):

    def __init__(self, locale):
        self.base = "https://www.google." + self.tldForLocale(locale)

        mnemory.SearchMnemory.__init__(self, locale)

    def getBaseUrl(self):
        return self.base + "/imghp"

    def getRequestUrl(self, q):
        return self.base + "/search?tbm=isch&q=%s" % quote(q)

    def getCompletions(self, q):

        def process(res):
            res = HTMLParser.HTMLParser().unescape(res.replace("<b>", "").replace("</b>", ""))
            return mnemory.CompletionResult(res)

        url = self.base + "/complete/search?client=img&hl=%s&gs_rn=43&gs_ri=img&ds=i&cp=1&gs_id=8&q=%%s" % self.langForLocale(self.locale)

        data = self.load_from_url(url, q)

        data = data.split("(", 1)[1][:-1]

        data = json.loads(data)

        return [process(x[0]) for x in data[1]]

class GoogleFinanceSearch(mnemory.SearchMnemory):

    def __init__(self, locale):
        self.base = "https://www.google." + self.tldForLocale(locale) + "/finance"

        mnemory.SearchMnemory.__init__(self, locale)

    def getBaseUrl(self):
        return self.base

    def getRequestUrl(self, q):
        return self.base + "?q=%s" % quote(q)

    def getCompletions(self, q):

         url = self.base + "/match?matchtype=matchall&q=%s"

         data = self.load_from_url(url, q)

         data = json.loads(data)['matches']

         def get_name(x):
            return x['t'] + " - " + x['n'] + " - " + x['e']

         return [mnemory.CompletionResult(get_name(x)) for x in data]

class GoogleTrendsSearch(mnemory.SearchMnemory):

    def __init__(self, locale):
        self.base = "https://www.google." + self.tldForLocale(locale) + "/trends"

        mnemory.SearchMnemory.__init__(self, locale)

    def getBaseUrl(self):
        return self.base

    def getRequestUrl(self, q):
        return self.base + "/explore#q=%s" % quote(q)

    def getCompletions(self, q):

        def parseResult(e):
            return mnemory.CompletionResult(e['title'], category=e['type'],
                    url=self.getRequestUrl(e['mid']))

        url = self.base + "/entitiesQuery?tn=10&q=%s"

        data = self.load_from_url(url, q)
        data = json.loads(data)

        try:
            res = [parseResult(x) for x in data['entityList']]
        except Exception as e:
            raise mnemory.CompletionParseError(self, data, e)

class Google(mnemory.MnemPlugin):

    def get_name(self):
        return "Google Searches"

    def report_mnemories(self):
        return {'google': GoogleSearch,
                'google-image': GoogleImageSearch,
                'google-finance': GoogleFinanceSearch,
                }
