#!flask/bin/python3

import argparse

from mnem import mnem, mnemory

from flask import Flask, jsonify
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

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

        mnemory = m.mnemories[key](locale)  # maybe opts too if we have other, engine specific setup to do?

        if not type:
            type = mnemory.getDefaultRequestType()

        if not type:
            raise ValueError("No search for the query found")  # TODO need a way to bail here

        res = mnemory.getRequestData(type, {'query': query})

        return res.getData()

ERRORS = {
    'internal': 1,
    'mnemory-not-found': 2,
    'completion-not-found': 3
}

ERROR_STR = {
    'internal': "Internal error",
    'mnemory-not-found': "Mnemory not found",
    'completion-not-found': "Completion not found",
}

def constructError(errKey, context):
    """
    Constructs a general error. Has at least the error code and
    description string, with an optional context if you have
    more details
    """

    try:
        err = {'error': {
            'code': ERRORS[errKey],
            'str' : ERROR_STR[errKey]
        }}
    except KeyError:
        # internal error if we can't even find the error key
        return constructError('internal', "Unknown error key: %s" % errKey)

    if (context):
        err['error']['context'] = context
    return err

class MnemoryCompletionAPI(Resource):

    def get(self, key, query, locale=None, completion=None):
        try:
            comps = m.complete(key, query, completion, locale)

        except mnem.MnemoryNotFoundError as e:
            return constructError('mnemory-not-found',
                                  {'mnemory': e.getMnemoryKey()})

        except mnemory.CompletionNotAvailableError as e:
            return constructError('completion-not-found',
                                  {'completion': e.getCompletion()})

        return {'completions': [self.completionResultJson(s) for s in comps]}

    def completionResultJson(self, c):
        """
        Convert a CompletionResult to json
        """
        # all completions have a keyword
        jc = {
            'keyword': c.keyword
        };

        if c.category:
            jc['category'] = c.category

        if c.url:
            jc['url'] = c.url

        if c.description:
            jc['desc'] = c.description

        return jc


api.add_resource(MnemoryListAPI, '/mnemory', endpoint='mnemories')

api.add_resource(MnemorySearchInfoAPI, '/search/<string:key>', endpoint='searchinfo')

api.add_resource(MnemorySearchAPI,
                 '/search/<string:key>/query/<string:query>',
                 '/search/<string:key>/<string:locale>/query/<string:query>',
                 '/search/<string:key>/type/<string:type>/query/<string:query>',
                 '/search/<string:key>/<string:locale>/type/<string:type>/query/<string:query>',
                 endpoint="search")

api.add_resource(MnemoryCompletionAPI,
                 '/complete/<string:key>/query/<string:query>',
                 '/complete/<string:key>/<string:locale>/query/<string:query>',
                 '/complete/<string:key>/type/<string:completion>/query/<string:query>',
                 '/complete/<string:key>/<string:locale>/type/<string:completion>/query/<string:query>',
                 endpoint='completion')

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
