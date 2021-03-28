from flask_restful import Resource


class Search(Resource):
    def get(self, topic_name=None):
        if not topic_name:
            return {
                'Operation': 'URL',
                'GET': '<address>:<port>/search/<topic_name>',
                'topic_name': 'include description'
            }

        # else call the catalog server

        return {
            'component': 'Search',
            'topicName': topic_name
        }


class LookUp(Resource):
    def get(self, item_id=None):
        if not item_id:
            return {
                'Operation': 'URL',
                'GET': '<address>:<port>/lookup/<item_id>',
                'item_id': 'include description'
            }

        # else call the catalog server

        return {
            'component': 'LookUp',
            'item_id': item_id
        }


class Buy(Resource):
    def post(self, item_id=None):
        if not item_id:
            return {
                'Operation': 'URL',
                'POST': '<address>:<port>/buy <<< {item_id: 1}',
                'topic_name': 'include description'
            }

        # else call the order server
        
        return {
            'component': 'Buy',
            'item_id': item_id    
        }