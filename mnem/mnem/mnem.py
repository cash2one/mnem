#! /usr/bin/env python

import os
# provide a default named log for package-wide use
import logging

logging.basicConfig(level=logging.ERROR)
PLUGIN_DIRS = [os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'plugins')]

from yapsy.PluginManager import PluginManager

class MnemError(Exception):
    pass

class MnemoryNotFoundError(MnemError):

    def __init__(self, mnemoryKey):
        self.key = mnemoryKey

    def __str__(self):
        return self.key

    def getMnemoryKey(self):
        return self.key

class MnemoryLocaleNotFound(MnemError):

    def __init__(self, key, locale):
        self.key = key
        self.locale = locale

    def __str__(self):
        return "%s: %s" % (self.key, self.locale)

class Mnem():

    def __init__(self):
        self.mnemories = {}

    def load_plugins(self):

        # Build the manager
        simplePluginManager = PluginManager()

        # Tell it the default place(s) where to find plugins
        simplePluginManager.getPluginLocator().updatePluginPlaces(PLUGIN_DIRS)
        # Load all plugins
        simplePluginManager.collectPlugins()

        # Activate all loaded plugins
        for plugin in simplePluginManager.getAllPlugins():
            # print("Importing plugin: %s" % plugin.plugin_object.get_name())

            mnemories = plugin.plugin_object.reportMnemories()
            # print("  Providing: %s" % mnemories)

            for m in mnemories:

                def getKey(mnemory):

                    if mnemory.defaultAlias:
                        return mnemory.defaultAlias

                    return self.key

                # TODO: allow to override aliases by configs?
                self.mnemories[getKey(m)] = m

    def dump_mnemories(self):

        import pprint

        p = pprint.PrettyPrinter()
        p.pprint(self.mnemories)

    def getMnemory(self, key, locale):
        try:
            m = self.mnemories[key]
        except KeyError:
            raise MnemoryNotFoundError(key)

        return m(locale)
