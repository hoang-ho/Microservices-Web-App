from flask import Flask
from flask_restful import Resource, Api

from api_list import Search, LookUp, Buy, UserList

app = Flask(__name__)
api = Api(app)

# route registration
api.add_resource(UserList, '/')

api.add_resource(Search, '/search', '/search/<topic_name>')
api.add_resource(LookUp, '/lookup', '/lookup/<item_id>')
api.add_resource(Buy, '/buy/<item_id>')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5004", debug=True)