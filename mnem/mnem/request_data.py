'''
Created on 3 Apr 2016

@author: John Beard
'''

class RequestData(object):
    '''
    Class to represent structured data related to a query. This could be one of
    (but not limited to):
      - URL to some external resource/web page (eg search engine results page
        for a given query)
      - Strutured list of search results of some kind (eg list of chemicals
        matching a certain string)
      - Structured data relating to a specific query on a database (eg list
        of properties for a given chemical)
    '''

    def __init__(self):
        pass

class PlainUrlReqData(RequestData):
    '''
    Request data that points a user to some external URL, with minimal extra 
    context
    
    This is likely to be  common data type for most "blind" queries, where
    Mnem just interpolates a string to a URL and the user goes to that page
    '''

    def __init__(self, url, title=None):
        self.url = url
        self.title = title

class CompletionReqData(RequestData):
    '''
    Request data representing a request that results in some list of 
    completions
    '''
    def __init__(self):
        pass