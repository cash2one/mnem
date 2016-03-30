'''
Created on 30 Mar 2016

@author: John Beard
'''

import os
import appdirs
import configparser

class ClientConfig(object):
    '''
    Class to read configs that apply to mnem clients in general, and provides
    defaults when not otherwise set
    '''
    app_name = "mnem"

    def __init__(self):
        
        # default set of configs
        defaults = {
            "complete": {
                "default": "google",
            },
            "search": {
                "default": "google"
            }
        }
    
        self._parser = configparser.ConfigParser(defaults)
        self.config = self._parser.read([])

    def find_user_config(self):
        '''
        Gets the default user config file if it exists, or None if not
        '''
        mnem_dir = appdirs.user_config_dir(self.app_name)
        
        if not os.path.isdir(mnem_dir):
            return None
        
        config_file = os.path.join(mnem_dir, "client.conf")
        
        if not os.path.isfile(config_file):
            return None
        
        return config_file
    
    def load_user_config(self):
        
        cfg_file = self.find_user_config()
        
        self._parser.read(cfg_file if cfg_file else [])

    def parser(self):
        return self._parser