'''
Created on 26 Feb 2016

@author: John Beard
'''

import requests

import mnem_rest_client.client_config as config

class MnemRestClient(object):
    '''
    A client to a Mnem REST server
    '''

    def __init__(self, serverUrl):

        cfg = config.ClientConfig()
        cfg.load_user_config()
        self.cfg = cfg.parser()

        self.url = serverUrl

    def connect(self):

        print("Connecting: %s" % self.url)

    def getCompletions(self, engineKey, locale, completion_type, query):

        # choose the end point
        url = '%s/search/%s' % (self.url, engineKey)

        if locale:
            url += '/%s' % locale

        if completion_type:
            url += "/type/%s" % completion_type

        url += "/query/%s" % (query);

        d = requests.get(url)

        # return empty for fail - maybe raise?
        if d.status_code != 200:
            return []

        try:
            return d.json()
        except:
            print("Json parse failed")
            return {}
