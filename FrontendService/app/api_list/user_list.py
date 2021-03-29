from flask_restful import Resource

class UserList(Resource):

    api_list = {
        'search': 'GET <address>:<port>/search/<topic_name>',
        'lookup': 'GET <address>:<port>/lookup/<item_id>',
        'buy': 'POST <address>:<port>/buy/<item_id>'
    }

    def get(self):
        return {
            'List': 'Available APIs',
            **self.api_list
        }