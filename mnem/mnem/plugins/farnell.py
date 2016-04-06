'''
Created on 3 Apr 2016

@author: John Beard
'''

from mnem import mnemory, locale, request_provider

from lxml.html import fromstring

class _FarnellComp(request_provider.SimpleUrlDataCompletion):

    def __init__(self, base):
        url = base + "/webapp/wcs/stores/servlet/AjaxSearchLookAhead?searchTerm=%s"
        super().__init__(url)

    def _can_process_query(self, opts):
        return len(opts['query']) > 2

    def _get_completions(self, data):
        cs = []

        root = fromstring(data)

        headings = root.findall("div")[1:-1]

        for h in headings:
            title = h.find("p").text
            listE = h.getnext()

            if listE.tag == 'ul':

                if "Categor" in title:
                    req_type = FarnellSearch.R_CATEGORY
                elif "Manufactur" in title:
                    req_type = FarnellSearch.R_MANUFACTURER
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
                                                           req_type=FarnellSearch.R_PRODUCT))

        return cs

class FarnellSearch(mnemory.SearchMnemory):

    key = "com.farnell.search"
    defaultAlias = "farnell"

    R_PRODUCT = 'product'
    R_MANUFACTURER = 'manufacturer'
    R_CATEGORY = 'category'

    def __init__(self, loc):
        super().__init__(loc)

        main_search = request_provider.UrlInterpolationProvider(self.getBaseUrl() + "/Search?st=%s")
        comp = _FarnellComp(self.getBaseUrl())
        comp.set_url_provider(main_search)

        manf_cat_search = request_provider.UrlInterpolationProvider(self.getBaseUrl() + "/%s")

        self.providers = {
                self.R_DEF_COMPLETE: comp,
                self.R_PRODUCT: main_search,
                self.R_MANUFACTURER: manf_cat_search,
                self.R_CATEGORY: manf_cat_search
        }

    def defaultLocale(self):
        return "us"

    def getBaseUrl(self):

        if self.locale == "us":
            return "https://www.newark.com"

        return "http://" + locale.domainForLocale(self.locale) + ".farnell.com"

class FarnellPlugin(mnemory.MnemPlugin):

    def getName(self):
        return "Farnell/Element14/Newark Searches"

    def reportMnemories(self):
        return [
            FarnellSearch
        ]
