import psycopg2
import json
#connection
con = psycopg2.connect(host="139.162.7.175",database= "nthrow_db",user="nthrow_reader",password="nthrow_reader_pw",port="5433")


cursor = con.cursor()

cursor.execute("select data->'email' from sites_2 limit 2")

rows = cursor.fetchall()

for row in rows:
    print(dict(row[0])['primary'])

cursor.close()
#close connection
con.close()