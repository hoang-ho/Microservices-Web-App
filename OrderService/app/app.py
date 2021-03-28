#coding: utf-8

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
app = Flask(__name__)
api = Api(app)
import sqlite3 as sql


def init_database():
    print('Creating database')
    conn = sql.connect('database.db')
    # print "Opened database successfully";
    conn.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
    conn.close()

    # print "Table created successfully";
@app.route('/hello')
def hello_google():
    #r= requests.get("http://localhost:5002/catalog", json={"id": 1})
    r = requests.get("http://catalog-service:5002/catalog", json={"id": 1})
    # r = requests.put("http://localhost:5002/catalog", json={"id": 1, "amount": -1})

    quantity = r.json()['Books'][0]['stock']
    print(quantity)
    if quantity > 0:
        print('Quantity')
        r = requests.put("http://catalog-service:5002/catalog", json={"id": 1, "amount": -1})
        print(r)
    #r = requests.get('http://www.google.com')

    return "Hello"

@app.route("/")
def hello():
    conn = sql.connect('database.db')
    # print "Opened database successfully";
    conn.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
    # print "Table created successfully";
    with sql.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO students (name,addr,city,pin) VALUES(?, ?, ?, ?)", ('app', 'b', 'c', 'd'))

        conn.commit()
        msg = "Record successfully added"
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall();
    for row in rows:
        print(row["name"], row["addr"], row["city"], row['pin'])
    #conn.close()
    #r = requests.put("http://localhost:5002/catalog", json={"id": 1, "amount": -1})
    #return str(r)
    return str(len(rows))

# @app.route("/buy")
# def buy_fun():
#      return render_template('index.html')

# @app.route('/parse', methods=['POST'])
# def parse():
#     if request.method == 'POST':
#         try:
#             id = request.form['id']
#             return str(len(id))

class OrderService(Resource):

    def get(self):
        request_data = request.get_json()

        return request_data

    def put(self):
        request_data = request.get_json()

        return request_data

api.add_resource(OrderService, "/order")


if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0',  port=5007)

