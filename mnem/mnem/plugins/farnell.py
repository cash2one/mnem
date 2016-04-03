'''
Created on 3 Apr 2016

@author: John Beard
'''

from mnem import mnemory, request_data

from lxml.html import fromstring
from urllib.parse import quote


class FarnellSearch(mnemory.SearchMnemory):

    key = "com.farnell.search"
    defaultAlias = "farnell"

    R_PRODUCT = 'product'
    R_MANUFACTURER = 'manufacturer'
    R_CATEGORY = 'category'

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
            self.R_PRODUCT,
            self.R_CATEGORY,
            self.R_MANUFACTURER
        ]

    def getRequestUrl(self, query, request):

        raise DeprecationWarning

    def getRequestData(self, req_type, options):

        try:
            query = options['query']
        except KeyError:
            # nneds a real exception
            raise ValueError("Expected a 'query' option: got %s" % options)

        if req_type in [self.R_CATEGORY, self.R_MANUFACTURER]:
            url = self.getBaseUrl() + "/" + query
        elif req_type == self.R_PRODUCT:
            url = self.getBaseUrl() + "/Search?st=%s" % quote(query)
        else:
            # make this a specific error
            raise ValueError("Unknown request type: %s" % req_type)

        return request_data.PlainUrlReqData(query, url)

    def defaultCompletionLoader(self, completion):
        api = self.getBaseUrl() + "/webapp/wcs/stores/servlet/AjaxSearchLookAhead?searchTerm=%s"
        return mnemory.completion.UrlCompletionDataLoader(api)

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

                if "Categor" in title:
                    req_type = self.R_CATEGORY
                elif "Manufactur" in title:
                    req_type = self.R_MANUFACTURER
                else:
                    # what is this heading? something new and exciting, no
                    # doubt
                    # some way to flag possible new things needed?
                    continue

                for a in listE.findall(".//a"):

                    url = a.get('href')
                    name = a.xpath("string()").strip()

                    try:
                        desc, name = name.rsplit(" > ", 1)
                    except ValueError:
                        desc = None

                    c.append(mnemory.CompletionResult(name, url=url,
                                                      category=title,
                                                      description=desc,
                                                      req_type=req_type))

            else:  # this is a product table
                for tr in listE.findall(".//tr"):
                    left = tr.find("td[@id='leftcolumn']/a")

                    url = left.get("href")
                    name = left.xpath("string()").strip()

                    desc = tr.find("td[@id='contentwrapper']/a").xpath("string()").strip()

                    c.append(mnemory.CompletionResult(name, url=url, category=title,
                                                       description=desc,
                                                       req_type=self.R_PRODUCT))

        return c

class FarnellPlugin(mnemory.MnemPlugin):

    def getName(self):
        return "Farnell/Element14/Newark Searches"

    def reportMnemories(self):
        return [
            FarnellSearch
        ]