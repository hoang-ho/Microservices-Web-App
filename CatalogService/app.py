from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database_setup import Base, Book
import json

app = Flask(__name__)
api = Api(app)

# Connect to Database and create database session
engine = create_engine('sqlite:///books-collection.db', echo=True)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def log_request(newData, key):
    f = open ('logfile.json', "r")
    data = json.loads(f.read())
    data[key].append(newData)
    fw = open('logfile.json', 'w')
    json.dump(data, fw)

@app.before_first_request
def prepopulate():
    app.logger.info("Prepopulate data")
    f = open ('logfile.json', "r")
    data = json.loads(f.read())

    # add all the book
    for book in data["add"]:
        session.add(Book(title=book["title"], topic=book["topic"], stock=book["stock"], cost=book["cost"]))
    
    session.commit()
    
    # update
    for book in data["update"]:
        session.query(Book).filter_by(id=book["id"]).update({"stock": book["stock"]})
    session.commit()

class CatalogService(Resource):
    def get(self):
        books = []
        request_data = request.get_json()
        app.logger.info("Receive a query request ")
        if (request_data):
            
            if ("id" in request_data):
                books = session.query(Book).filter_by(id=request_data["id"]).all()
                logRequest = {"id": request_data["id"]}
                log_request(logRequest, "get")
                response = jsonify(Books=[book.serialize for book in books])
                response.status_code = 200
                return response

            elif ("topic" in request_data):
                books = session.query(Book).filter_by(topic=request_data["topic"]).all()
                logRequest = {"topic": request_data["topic"]}
                log_request(logRequest, "get")
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
        if ("id" in data):
            book = session.query(Book).filter_by(id=data["id"]).one()
            book.stock -= 1
            logRequest = {"id": book.id, "stock": book.stock}
            log_request(logRequest, "update")
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