import sqlite3 as sql

conn = sql.connect('database.db')
# print "Opened database successfully";
conn.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
# print "Table created successfully";
with sql.connect("database.db") as conn:
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name,addr,city,pin) VALUES(?, ?, ?, ?)",('x','b','c','d') )

    conn.commit()
con = sql.connect("database.db")
con.row_factory = sql.Row

cur = con.cursor()
cur.execute("select * from students")

rows = cur.fetchall();
for row in rows:
    print(row["name"], row["addr"],row["city"],row['pin'])