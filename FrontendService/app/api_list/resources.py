from flask_restful import Resource

import requests

class Search(Resource):
    def get(self, topic_name=None):
        if not topic_name:
            return {
                'Operation': 'URL',
                'GET': '<address>:<port>/search/<topic_name>',
                'topic_name': 'include description'
            }

        if(topic_name == 'distributed-systems'):
            data = {"topic": "distributed systems"}
        elif(topic_name == 'graduate-school'):
           data = {"topic": "graduate school"}
        else:
            return {"message": "topic name should be in [distributed-systems, graduate-school"}, 400     
        
        response = requests.get('http://catalog-service:5002/catalog/query', json=data)
        return response.json()


class LookUp(Resource):
    def get(self, item_id=None):
        if not item_id:
            return {
                'Operation': 'URL',
                'GET': '<address>:<port>/lookup/<item_id>',
                'item_id': 'include description'
            }

        data = {"id": int(item_id)}

        response = requests.get('http://catalog-service:5002/catalog/query', json=data)
        return response.json()


class Buy(Resource):
    def post(self, item_id=None):
        if not item_id:
            return {
                'Operation': 'URL',
                'PUT': '<address>:<port>/buy <<< {item_id: 1}',
                'topic_name': 'include description'
            }

        data = {"id": int(item_id)}

        response = requests.put('http://order-service:5007/order', json=data)
        return response.json()