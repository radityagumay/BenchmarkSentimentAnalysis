import mysql.connector
import csv
from HTMLParser import HTMLParser
import requests

csv.field_size_limit(500 * 1024 * 1024)

db = mysql.connector.connect(user='root', password='',
                             host='127.0.0.1',
                             database='sentiment_analysis')
cursor = db.cursor()

table_name = "review"
collection = "collection.csv"
url = 'http://text-processing.com/demo/sentiment/'


class Parser(HTMLParser):
    def __init__(self, review_id, review_name, review_body):
        print "id", review_id
        print "reviewName", review_name
        print "reviewBody", review_body

        HTMLParser.__init__(self)
        payload = {'language': 'english', 'text': review_body}
        self.request = requests.post(url, data=payload)
        self.feed(self.request.text)

    def handle_data(self, data):
        if "pos:" in data:
            positive = data.split(None)
            print positive[1]
        elif "pos" in data:
            print "sentiment is positive"

        if "neg:" in data:
            negative = data.split(None)
            print negative[1]
        elif "neg" in data:
            print "sentiment is negative"

        if "neutral:" in data:
            neutral = data.split(None)
            print neutral[1]
        elif "neutral" in data:
            print "sentiment is neutral"

        if "polar:" in data:
            polarity = data.split(None)
            print polarity[1]


# def insert(document):
#    query = "INSERT INTO " + table_name + " VALUES (" + query_plain + ")"
#    cursor.execute(query)
#    db.commit()


def do_sentiment_analysis(review_id, review_name, review_body):
    Parser(review_id, review_name, review_body)


with open(collection, 'rb') as csvfile:
    documents = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in documents:
        doc = ' '.join(row)
        doc_array = doc.split(',')
        reviewId = doc_array[0]
        reviewName = doc_array[3]
        reviewBody = doc_array[4]
        do_sentiment_analysis(reviewId, reviewName, reviewBody)

db.close()
