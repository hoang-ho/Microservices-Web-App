from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database_setup import Base, Book

app = Flask(__name__)
api = Api(app)

# Connect to Database and create database session
engine = create_engine('sqlite:///books-collection.db', echo=True)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.before_first_request
def prepopulate():
    app.logger.info("Prepopulate data")
    session.add_all([
        Book(title="How to get a good grade in 677 in 20 minutes a day.", topic="distributed systems", stock = 3),
        Book(title="RPCs for Dummies.", topic="distributed systems", stock = 3),
        Book(title="Xen and the Art of Surviving Graduate School.", topic="graduate school", stock = 3),
        Book(title="Cooking for the Impatient Graduate Student.", topic="graduate school", stock = 3)
    ])
    session.commit()

class CatalogService(Resource):
    def get(self):
        books = []
        request_data = request.get_json()
        app.logger.info("Receive a query request ")
        if (request_data):
            if ("title" in request_data):
                books = session.query(Book).filter_by(title=request_data["title"]).all()
                response = jsonify(Books=[book.serialize for book in books])
                response.status_code = 200
                return response

            elif ("topic" in request_data):
                books = session.query(Book).filter_by(topic=request_data["topic"]).all()
                response = jsonify(Books=[book.serialize for book in books])
                response.status_code = 200
                return response
        else:
            response = jsonify(success=False)
            response.status_code = 400
            return response
    
    def put(self):
        app.logger.info("Receive a update request")
        data = request.get_json()
        app.logger.info("Receive a query request " + str(data))
        if ("id" in data and "amount" in data):
            book = session.query(Book).filter_by(id=data["id"]).one()
            book.stock += data["amount"]
            response = jsonify(success=True)
            response.status_code = 200
            return response
        else:
            response = jsonify(success=False)
            response.status_code = 400
            return response

api.add_resource(CatalogService, "/catalog")

if __name__ == "__main__":
    # run the application
    app.debug = True
    app.run(host='0.0.0.0', port=5002)