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


class MnemorySearchAPI(MnemoryAPI):

    def get(self, key, query, locale = None):
        mnemory = m.mnemories[key](locale)
        return {'url': str(mnemory.submitSearch(query))}

class MnemoryCompletionAPI(MnemoryAPI):

    def get(self, key, query, locale = None):
        mnemory = m.mnemories[key](locale)
        return {'completions': [self.completionResultJson(s) for s in mnemory.submitForSuggestions(query)]}

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

api.add_resource(MnemoryListAPI, '/mnemory', endpoint='mnemories')
api.add_resource(MnemorySearchAPI, '/search/<string:key>/<string:query>', endpoint='url')
api.add_resource(MnemoryCompletionAPI, '/complete/<string:key>/<string:query>', endpoint='completions')

if __name__ == '__main__':
    print("Mnem server")
    app.run(debug=True)
