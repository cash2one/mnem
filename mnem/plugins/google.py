#! /usr/bin/env python

import mnemory

import json
import urllib2

class GoogleSearch(mnemory.SearchMnemory):

    def getBaseUrl(self):
        return "https://www.google.com"

    def getRequestUrl(self, q):
        return "https://www.google.com/search?q=%s" % q

    def getCompletions(self, q):

        url = "https://www.google.com/complete/search?client=chrome-omni&gs_ri=chrome-ext&oit=1&cp=1&pgcl=7&q=%s" % q

        data = urllib2.urlopen(url).read()

        data = json.loads(data)

        return [mnemory.CompletionResult(x) for x in data[1]]

class GoogleImageSearch(mnemory.SearchMnemory):

    def __init__(self, locale):
        self.base = "https://www.google." + self.tldForLocale(locale)

        mnemory.SearchMnemory.__init__(self, locale)

    def getBaseUrl(self):
        return self.base + "/imghp"

    def getRequestUrl(self, q):
        return self.base + "/search?tbm=isch&q=%s" % q

    def getCompletions(self, q):

        url = self.base + "/complete/search?client=img&hl=%s&gs_rn=43&gs_ri=img&ds=i&cp=1&gs_id=8&q=%s" % (self.langForLocale(self.locale), q)

        data = urllib2.urlopen(url).read()

        data = data.split("(", 1)[1][:-1]

        data = json.loads(data)

        return [mnemory.CompletionResult(x[0].replace("<b>", "").replace("</b>", "")) for x in data[1]]

class Google(mnemory.MnemPlugin):

    def get_name(self):
        return "Google Searches"

    def report_mnemories(self):
        return {'google': GoogleSearch,
                'google-image': GoogleImageSearch
                }
