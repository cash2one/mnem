#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mnem import mnemory
from urllib.parse import quote, unquote
import json

from lxml.html import fromstring

class OctopartSearch(mnemory.SearchMnemory):

    key = "com.octopart.search"
    defaultAlias = "octopart"

    base = "https://octopart.com"

    def __init__(self, locale):
        mnemory.SearchMnemory.__init__(self, None)

    def getRequestUrl(self, q):
        return self.base + "/search?q=" + quote(q)

    def availableCompletions(self):
        return ["default"]

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

class MouserSearch(mnemory.SearchMnemory):

    key = "com.mouser.search"
    defaultAlias = "mouser"

    def __init__(self, locale):
        mnemory.SearchMnemory.__init__(self, None)

    def availableCompletions(self):
        return ["default"]

    def getBaseUrl(self):
        return "http://" + self.domainForLocale(self.locale) + ".mouser.com"

    def getRequestUrl(self, q):
        return self.getBaseUrl() + "/Search/Refine.aspx?Keyword=%s" % quote(q)

    def getCompletions(self, completion, q):

        def parse(entry):

            kwd, uid = entry['value'].split("##", 1)

            return mnemory.CompletionResult(kwd.strip(), url= uidUrl % uid)

        api = self.getBaseUrl() + "/ajax/autosuggestion.ashx?q=%s"
        uidUrl = self.getBaseUrl() + "/Search/Refine.aspx?N=%s"

        result = self.load_from_url(api, q).json()

        print(result)

        return [parse(e) for e in result]

class FarnellSearch(mnemory.SearchMnemory):

    key = "com.farnell.search"
    defaultAlias = "farnell"

    def __init__(self, locale):
        mnemory.SearchMnemory.__init__(self, None)

    def defaultLocale(self):
        return "us"

    def availableCompletions(self):
        return ["default"]

    def getBaseUrl(self):

        if self.locale == "us":
            return "https://www.newark.com"

        return "http://" + self.domainForLocale(self.locale) + ".farnell.com"

    def getRequestUrl(self, q):
        return self.getBaseUrl() + "/Search?st=%s" % quote(q)

    def getCompletions(self, completion, q):

        if (len(q) <= 2):
            # this API doesn't work for short queries
            return []

        api = self.getBaseUrl() + "/webapp/wcs/stores/servlet/AjaxSearchLookAhead?searchTerm=%s"

        result = self.load_from_url(api, q)
        root = fromstring(result.text)

        headings = root.findall("div")[1:-1]

        c = []

        for h in headings:
            title = h.find("p").text
            listE = h.getnext()

            if listE.tag == 'ul':

                for a in listE.findall(".//a"):

                    url = a.get('href')
                    name = a.xpath("string()").strip()

                    try:
                        desc, name = name.rsplit(" > ", 1)
                    except ValueError:
                        desc = None

                    c.append(mnemory.CompletionResult(name, url=url, category=title, description=desc))

            else: # this is a product table
                for tr in listE.findall(".//tr"):
                    left = tr.find("td[@id='leftcolumn']/a")

                    url = left.get("href")
                    name = left.xpath("string()").strip()

                    desc = tr.find("td[@id='contentwrapper']/a").xpath("string()").strip()

                    c.append(mnemory.CompletionResult(name, url=url, category=title, description=desc))

        return c

class ElectronicsSupply(mnemory.MnemPlugin):

    def get_name(self):
        return "Electronics Supply Searches"

    def report_mnemories(self):
        return [
            OctopartSearch,
            MouserSearch,
            FarnellSearch
        ]
