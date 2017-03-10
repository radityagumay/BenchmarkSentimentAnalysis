import mysql.connector
import csv
csv.field_size_limit(500 * 1024 * 1024)

db = mysql.connector.connect(user='root', password='',
                             host='127.0.0.1',
                             database='google_play_crawler')

cur = db.cursor()

collection = "collection.csv"

with open(collection, 'rb') as csvfile:
    documents = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in documents:
        doc = ' '.join(row)
        doc_array = doc.split(',')
        for array in doc_array:
            token = array
            print token


#cur.execute("SELECT * FROM authors")
#for row in cur.fetchall():
#    print row[0], row[3], row[4]

db.close()
