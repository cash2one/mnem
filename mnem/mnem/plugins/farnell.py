'''
Created on 3 Apr 2016

@author: John Beard
'''

from mnem import mnemory, request_data

from lxml.html import fromstring
from urllib.parse import quote

class UrlLoaderWithMinLength(mnemory.completion.UrlCompletionDataLoader):

    def __init__(self, minlen, *args, **kwargs):
        self.minlen = minlen
        super(UrlLoaderWithMinLength, self).__init__(*args, **kwargs)

    def load(self, query):

        if len(query) < self.minlen:
            raise mnemory.RequestLoaderNullRequest(query)

        return super(UrlLoaderWithMinLength, self).load(query)

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
        return [self.R_DEF_COMPLETE]

    def availableRequests(self):
        return [
            self.R_PRODUCT,
            self.R_CATEGORY,
            self.R_MANUFACTURER
        ]

    def getBaseUrl(self):

        if self.locale == "us":
            return "https://www.newark.com"

        return "http://" + self.domainForLocale(self.locale) + ".farnell.com"

    def _getSearchLoader(self, req_type):

        if req_type == self.R_DEF_COMPLETE:
            api = self.getBaseUrl() + "/webapp/wcs/stores/servlet/AjaxSearchLookAhead?searchTerm=%s"
            return UrlLoaderWithMinLength(3, api)

    def _getRequestData(self, req_type, options, data):

        if req_type == self.R_DEF_COMPLETE:
            cs = self._getCompletions(data)
            return mnemory.request_data.CompletionReqData(cs)
        else:
            return self._urlData(req_type, options)

    def _urlData(self, req_type, options):

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

    def _getCompletions(self, data):

        cs = []

        root = fromstring(data)

        headings = root.findall("div")[1:-1]

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

                    cs.append(mnemory.CompletionResult(name, url=url,
                                                      category=title,
                                                      description=desc,
                                                      req_type=req_type))

            else:  # this is a product table
                for tr in listE.findall(".//tr"):
                    left = tr.find("td[@id='leftcolumn']/a")

                    url = left.get("href")
                    name = left.xpath("string()").strip()

                    desc = tr.find("td[@id='contentwrapper']/a").xpath("string()").strip()

                    cs.append(mnemory.CompletionResult(name, url=url,
                                                           category=title,
                                                           description=desc,
                                                           req_type=self.R_PRODUCT))

        return cs

class FarnellPlugin(mnemory.MnemPlugin):

    def getName(self):
        return "Farnell/Element14/Newark Searches"

    def reportMnemories(self):
        return [
            FarnellSearch
        ]
