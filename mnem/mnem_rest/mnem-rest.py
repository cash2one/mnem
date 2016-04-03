#!flask/bin/python3

import argparse

from mnem import mnem, mnemory
from mnem_rest import errors

from flask import Flask, jsonify
from flask.ext.restful import Api, Resource

"""RESTful Mnem server"""

m = mnem.Mnem()
m.load_plugins()

app = Flask(__name__, static_url_path="")
api = Api(app)
m.dump_mnemories()

class MnemoryListAPI(Resource):

    def get(self):

        def presentMnemory(key):
            return {
                'key': key
            }

        return {'mnemories': [presentMnemory(mnemory) for mnemory in m.mnemories]}

class MnemorySearchInfoAPI(Resource):

    def get(self, key, locale=None):
        mnemory = m.mnemories[key](locale)

        jc = {
            'key': key,
            'completions': mnemory.availableCompletions(),
            'searches': mnemory.availableRequests()  # TODO need to add more info here
        }

        return jc

class MnemorySearchAPI(Resource):

    def get(self, key, query, type=None, locale=None):

        try:
            mnemory = m.getMnemory(key, locale)

        except mnem.MnemoryNotFoundError as e:
            return errors.constructError('mnemory-not-found',
                                  {'mnemory': key})
        except mnem.MnemoryLocaleNotFound:
            return errors.constructError('locale-not-found',
                                  {'mnemory': key,
                                   'locale': locale
                                  })

        if not type:
            type = mnemory.getDefaultRequestType()

        if not type:
            return errors.constructError('request-type-not-found',
                                         {'type': type})

        res = mnemory.getRequestData(type, {'query': query})

        return res.getData()

api.add_resource(MnemoryListAPI, '/mnemory', endpoint='mnemories')

api.add_resource(MnemorySearchInfoAPI, '/search/<string:key>', endpoint='searchinfo')

api.add_resource(MnemorySearchAPI,
                 '/search/<string:key>/query/<string:query>',
                 '/search/<string:key>/<string:locale>/query/<string:query>',
                 '/search/<string:key>/type/<string:type>/query/<string:query>',
                 '/search/<string:key>/<string:locale>/type/<string:type>/query/<string:query>',
                 endpoint="search")

if __name__ == '__main__':

    defualtPort = 27183

    parser = argparse.ArgumentParser(description='Run the Mnem REST server')

    parser.add_argument('-p', '--port', dest='port', action='store',
                   metavar='PORT', default=defualtPort, type=int,
                   help='the port to run the REST interface on (default=%d)' % defualtPort)
    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                   help='run in debug mode')

    args = parser.parse_args()

    print("Mnem server on port %d" % args.port)

    app.run(debug=args.debug, port=args.port)
