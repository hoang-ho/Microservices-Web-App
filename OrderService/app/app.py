#coding: utf-8

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json
import requests
app = Flask(__name__)
api = Api(app)
import sqlite3 as sql
from datetime import datetime

@app.before_first_request
def init_database():
    conn = sql.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS buy_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, request_id INTEGER NOT NULL, timestamp TEXT NOT NULL)')
    conn.close()


class LogService(Resource):
    def get(self):
        with sql.connect("database.db") as conn:
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute("select * from buy_logs")
            rows = cur.fetchall()
            row_list=[]
            for row in rows:
                row_list.append({'id':row['id'],'request_id':row['request_id'],'timestamp':row['timestamp']})
        if rows:
            result=json.dumps(row_list)
        else:
            result=json.dumps( {'message': 'Log is empty'})
        return result

class OrderService(Resource):

    def put(self):
        request_data = request.get_json()
        id= request_data['id']
        if not id:
            return json.dumps({'message':"Invalid request"})

        with sql.connect("database.db") as conn:
             cur = conn.cursor()
             time_stamp = str(datetime.now())
             cur.execute("INSERT INTO buy_logs (request_id,timestamp) VALUES( ?, ?)",  (id,time_stamp ))
             conn.commit()
        response = requests.get("http://catalog-service:5002/catalog", json={"id": id})
        response_json= response.json()
        if response.status_code!=200:
            return json.dumps({'message': "Error in receiving response from catalog service"})
        if len(response_json['Books']) > 0:
            quantity = response_json['Books'][0]['stock']
        else:
            return json.dumps({'message': "Invalid request id"})

        if quantity > 0:
            response = requests.put("http://catalog-service:5002/catalog", json={"id": id, "amount": -1})
            if response.status_code== 200:
                return json.dumps({'message': 'Buy request successful'})
            else:
                return json.dumps({'message': 'Buy request falied'})

        #     # print(r)
        # # r = requests.get('http://www.google.com')
        else:
            return json.dumps({'message': 'Item not available'})


        return json.dumps({'message': 'Error while buying'})

        #return request_data

api.add_resource(OrderService, "/order")
api.add_resource(LogService, "/log")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',  port=5007)

