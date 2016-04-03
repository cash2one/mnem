'''
Created on 3 Apr 2016

@author: John Beard
'''

from mnem import mnemory

from lxml.html import fromstring
from urllib.parse import quote


class FarnellSearch(mnemory.SearchMnemory):

    key = "com.farnell.search"
    defaultAlias = "farnell"

    def __init__(self, locale):
        mnemory.SearchMnemory.__init__(self, locale)

    def defaultLocale(self):
        return "us"

    def availableCompletions(self):
        return ["default"]

    def getBaseUrl(self):

        if self.locale == "us":
            return "https://www.newark.com"

        return "http://" + self.domainForLocale(self.locale) + ".farnell.com"

    def availableRequests(self):
        return [
            'product',
            'manufacturer',
            'category'
        ]

    def getRequestUrl(self, query, request):

        if request == 'manufacturer':
            url = self.getBaseUrl() + "/" + query
        elif request == 'category':
            url = self.getBaseUrl() + "/" + query
        elif request == 'product':
            url = self.getBaseUrl() + "/Search?st=%s" % quote(query)
        else:
            raise ValueError

        return url

    def defaultCompletionLoader(self, completion):
        api = self.getBaseUrl() + "/webapp/wcs/stores/servlet/AjaxSearchLookAhead?searchTerm=%s"
        return completion.UrlCompletionDataLoader(api)

    def providesCompletionsForQuery(self, query, completion):
        # farnell only resposnds to queries of 3 or more chars
        return len(query) > 2

    def getCompletions(self, data):

        root = fromstring(data)

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

            else:  # this is a product table
                for tr in listE.findall(".//tr"):
                    left = tr.find("td[@id='leftcolumn']/a")

                    url = left.get("href")
                    name = left.xpath("string()").strip()

                    desc = tr.find("td[@id='contentwrapper']/a").xpath("string()").strip()

                    c.append(mnemory.CompletionResult(name, url=url, category=title, description=desc))

        return c
