from flask_restful import Resource

import requests

class Search(Resource):
    def get(self, topic_name=None):
        if not topic_name:
            return {
                'Operation': 'URL',
                'GET': '<address>:<port>/search/<topic_name>',
                'topic_name': 'a string of the value distributed-systems or graduate-school'
            }

        if(topic_name == 'distributed-systems'):
            data = {"topic": "distributed systems"}
        elif(topic_name == 'graduate-school'):
           data = {"topic": "graduate school"}
        else:
            return {"message": "topic name should be in [distributed-systems, graduate-school]"}, 400     
        
        try:
            response = requests.get('http://catalog-service:5002/catalog/query', json=data)
            if response.status_code == 200:
                return response.json()
        except:
            return {'message': 'something went wrong. Please try again'}, 500


class LookUp(Resource):
    def get(self, item_id=None):
        if not item_id:
            return {
                'Operation': 'URL',
                'GET': '<address>:<port>/lookup/<item_id>',
                'item_id': 'string that specifies the book id. It accepts value from 1 to 4'
            }

        id = int(item_id)
        if(id > 4 or id < 1):
            return {"message": "Please enter a correct id"}, 400  

        data = {"id": id}

        try:
            response = requests.get('http://catalog-service:5002/catalog/query', json=data)
            if response.status_code == 200:
                return response.json()
        except:
            return {'message': 'something went wrong. Please try again'}, 500
        

class Buy(Resource):
    def post(self, item_id=None):
        if not item_id:
            return {
                'Operation': 'URL',
                'POST': '<address>:<port>/buy/<item_id>',
                'topic_name': 'string that specifies the book id. It accepts value from 1 to 4'
            }

        id = int(item_id)
        if(id > 4 or id < 1):
            return {"message": "Please enter a correct id"}, 400  

        data = {"id": id}

        try:
            response = requests.put('http://order-service:5007/order', json=data)
            if response.status_code == 200:
                return {'message': 'book bought successful'}
        except:
            return {'message': 'something went wrong. Please try again'}, 500
