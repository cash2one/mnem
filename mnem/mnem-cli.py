import mnem

if __name__ == '__main__':
    m = mnem.Mnem()
    m.load_plugins()

    key = 'google-finance'
    query= "dra"
    locale = 'uk'
    #locale = None

    r = m.complete(key, query, locale)

    if r:
        print [str(x) for x in r]

    r = m.search(key, query, locale)

    print r
