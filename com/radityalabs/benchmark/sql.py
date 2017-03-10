import mysql.connector

db = mysql.connector.connect(user='root', password='',
                             host='127.0.0.1',
                             database='google_play_crawler')

cur = db.cursor()
cur.execute("SELECT * FROM authors")
for row in cur.fetchall():
    print row[0], row[3], row[4]

db.close()
