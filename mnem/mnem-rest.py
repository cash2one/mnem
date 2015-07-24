#!flask/bin/python3

import mnem

from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

"""RESTful Mnem server"""

m = mnem.Mnem()
m.load_plugins()

app = Flask(__name__, static_url_path="")
api = Api(app)

mnemory_fields = {
    'key': fields.String,
    'description': fields.String,
}

class MnemoryListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
        super(MnemoryListAPI, self).__init__()

    def get(self):
        return {'mnemories': [marshal(mnemory, mnemory_fields) for mnemory in m.mnemories]}

class MnemoryAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('query', type=str, required=True, location='json')
        self.reqparse.add_argument('key', type=str, required=True, default="", location='json')
        super(MnemoryAPI, self).__init__()

class MnemorySearchInfoAPI(MnemoryAPI):

    def get(self, key, locale = None):
        mnemory = m.mnemories[key](locale)

        jc = {
            'key': key,
            'completions': mnemory.availableCompletions()
        }

        return jc

class MnemorySearchQueryAPI(MnemoryAPI):

    def get(self, key, query, locale = None):
        mnemory = m.mnemories[key](locale)

        jc = {
            'url': str(mnemory.getSearchForQuery(query))
        }

        return jc


class MnemoryCompletionLocaleAPI(MnemoryAPI):

    def get(self, key, completion, query, locale):
        mnemory = m.mnemories[key](locale)

        comps = mnemory.submitForSuggestions(completion, query)
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

        return jc

class MnemoryCompletionAPI(MnemoryCompletionLocaleAPI):

    def get(self, key, completion, query, locale):
        return MnemoryCompletionLocaleAPI.get(key, completion, query, None)

api.add_resource(MnemoryListAPI, '/mnemory', endpoint='mnemories')
api.add_resource(MnemorySearchInfoAPI, '/search/<string:key>', endpoint='searchinfo')
api.add_resource(MnemorySearchQueryAPI, '/search/<string:key>/query/<string:query>', endpoint='searchquery')
api.add_resource(MnemoryCompletionAPI, '/complete/<string:key>/<string:completion>/<string:query>', endpoint='completions')
api.add_resource(MnemoryCompletionLocaleAPI, '/complete/<string:key>/<string:completion>/locale/<string:locale>/<string:query>', endpoint='completions_locale')


if __name__ == '__main__':
    print("Mnem server")
    app.run(debug=True)
