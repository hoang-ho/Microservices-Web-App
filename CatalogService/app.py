from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database_setup import Base, Book
import json
import time

app = Flask(__name__)
api = Api(app)

# Connect to Database and create database session
engine = create_engine('sqlite:///books-collection.db', echo=True)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def log_request(newData, key):
    fd = open('logfile.json', "r+")
    data = json.loads(fd.read())
    data[key].append(newData)
    fd.seek(0)
    json.dump(data, fd)
    fd.truncate()
    fd.close()


@app.before_first_request
def prepopulate():
    app.logger.info("Prepopulate data")
    if (session.query(Book).first() is None):
        f = open('logfile.json', "r")
        data = json.loads(f.read())

        # add all the book
        for book in data["add"]:
            session.add(Book(
                title=book["title"], topic=book["topic"], stock=book["stock"], cost=book["cost"]))
        session.commit()

        # update
        for book in data["buy"]:
            session.query(Book).filter_by(
                id=book["id"]).update({"stock": book["stock"]})
        session.commit()


class Query(Resource):
    def get(self):
        books = []
        request_data = request.get_json()
        app.logger.info("Receive a query request ")
        if (request_data):

            if ("id" in request_data):
                books = session.query(Book).filter_by(
                    id=request_data["id"]).all()
                logRequest = {
                    "id": request_data["id"], "timestamp": time.time()}
                log_request(logRequest, "query")
                response = jsonify(
                    Books=[book.serializeQueryById for book in books])
                response.status_code = 200
                return response

            elif ("topic" in request_data):
                books = session.query(Book).filter_by(
                    topic=request_data["topic"]).all()
                logRequest = {
                    "topic": request_data["topic"], "timestamp": time.time()}
                log_request(logRequest, "query")
                response = jsonify(
                    items=[book.serializeQueryByTopic for book in books])
                response.status_code = 200
                return response
        else:
            response = jsonify(success=False)
            response.status_code = 400
            return response


class Buy(Resource):
    def put(self):
        app.logger.info("Receive a buy request")
        data = request.get_json()
        if ("id" in data):
            book = session.query(Book).filter_by(id=data["id"]).one()
            book.stock -= 1
            logRequest = {"id": book.id, "stock": book.stock,
                          "timestamp": time.time()}
            log_request(logRequest, "buy")
            response = jsonify(success=True)
            response.status_code = 200
            return response
        else:
            response = jsonify(success=False)
            response.status_code = 400
            return response


api.add_resource(Query, "/catalog/query")
api.add_resource(Buy, "/catalog/update")

if __name__ == "__main__":
    # run the application
    app.debug = True
    app.run(host='0.0.0.0', port=5002)
