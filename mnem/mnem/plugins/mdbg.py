'''
Created on 6 Apr 2016

@author: John Beard
'''

from json import loads

from mnem import mnemory, request_provider

class _MdbgCompl(request_provider.SimpleUrlDataCompletion):

    def __init__(self):

        url = 'http://www.mdbg.net/chindict/chindict_ac_wdqb.php?st=0&l=15&i=%s'
        super().__init__(url)

    def _get_completions(self, data):

        data = loads(data)
        keys = [s['value'] for s in data]

        return [mnemory.CompletionResult(key) for key in keys]

class MdbgSearch(mnemory.SearchMnemory):

    key = "net.mdbg.search"
    defaultAlias = "mdbg"

    def __init__(self, locale=None):
        super().__init__(locale)

        s_url = 'http://www.mdbg.net/chindict/chindict.php?page=worddict&wdqb=%s'

        search = request_provider.UrlInterpolationProvider(s_url)
        comp = _MdbgCompl()

        self._add_basic_search_complete(search, comp)

class MDBG(mnemory.MnemPlugin):

    def getName(self):
        return "Mdbg Searches"

    def reportMnemories(self):
        return [
            MdbgSearch
        ]

