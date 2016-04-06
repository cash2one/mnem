'''
Created on 6 Apr 2016

@author: John Beard
'''

def tldForLocale(locale):
    try:
        tld = {
            'uk': 'co.uk',
            'fr': 'fr'
        }[locale]
    except KeyError:
        tld = 'com'

    return tld

def langForLocale(locale):
    try:
        tld = {
            'uk': 'en',
            'fr': 'fr'
        }[locale]
    except KeyError:
        tld = 'en'

    return tld

def domainForLocale(locale):

    try:
        domain = {
            'uk': "uk",
            'jp': "jp",
            'aus': "au",
        }[locale]
    except KeyError:
        domain = "us"

    return domain
