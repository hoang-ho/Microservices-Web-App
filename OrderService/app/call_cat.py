import requests
import sqlite3 as sql

def buy(id):
    r= requests.get("http://localhost:5002/catalog", json={"id": id}).json()
    quantity=r['Books'][0]['stock']
    print(quantity)
    if quantity>0:
        print('Quantity')
        r=requests.put("http://localhost:5002/catalog", json={"id": id, "amount": -1})
        print(r)
    with sql.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO students (name,addr,city,pin) VALUES(?, ?, ?, ?)", ('app', 'b', 'c', 'd'))
        conn.commit()

    # con = sql.connect("database.db")
    # con.row_factory = sql.Row
    #
    # cur = con.cursor()
    # cur.execute("select * from students")
    #
    # rows = cur.fetchall();
    # for row in rows:
    #     print(row["name"], row["addr"], row["city"], row['pin'])

if __name__ == '__main__':
    print(buy(2))
