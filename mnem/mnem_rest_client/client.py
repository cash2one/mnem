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
        
    def getCompletions(self, engineKey, completion, query):
        
        # choose the end point
        if completion:
            url = self.url + "/complete/%s/%s/%s" % (engineKey, completion, query);
        else:
            url = self.url + "/complete/%s/%s" % (engineKey, query);
        
        d = requests.get(url)
        
        # return empty for fail - maybe raise?
        if d.status_code != 200:
            return []
        
        try:
            return d.json()
        except:
            print("Json parse failed")
            return {}