import mysql.connector
import csv
import requests
import sys

from BeautifulSoup import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')
csv.field_size_limit(500 * 1024 * 1024)

db = mysql.connector.connect(user='root', password='',
                             host='127.0.0.1',
                             database='sentiment_analysis')
cursor = db.cursor()

table_name = "review_label_benchmark"
collection = "full_collection.csv"
url = 'http://text-processing.com/demo/sentiment/'


class Parser:
    def __init__(self, review_id, review_name, review_body):
        self.review_id = review_id
        self.review_name = review_name
        self.review_body = review_body
        print "id", self.review_id
        print "reviewName", self.review_name
        print "reviewBody", self.review_body

        payload = {'language': 'english', 'text': review_body}
        try:
            self.request = requests.post(url, data=payload)
        except requests.exceptions.RequestException as e:
            print "run service again", e
            print run()
            return

        self.html = BeautifulSoup(self.request.text)
        self.sentiment_collection = self.html.body.find('div', attrs={'class': 'span-9 last'})
        self.collection_sentiment = self.sentiment_collection.findAll('li')
        self.positive_value = "0"
        self.negative_value = "0"
        self.neutral_value = "0"
        self.polarity_value = "0"
        for item in self.collection_sentiment:
            self.sentiment_result = item.text
            if "pos:" in self.sentiment_result:
                self.positive = self.sentiment_result.split(None)
                self.positive_value = self.positive[1]
                print "positive", self.positive_value
            if "neg:" in self.sentiment_result:
                self.negative = self.sentiment_result.split(None)
                self.negative_value = self.negative[1]
                print "negative", self.negative_value
            if "neutral:" in self.sentiment_result:
                self.neutral = self.sentiment_result.split(None)
                self.neutral_value = self.neutral[1]
                print "neutral", self.neutral_value
            if "polar:" in self.sentiment_result:
                self.polarity = self.sentiment_result.split(None)
                self.polarity_value = self.polarity[1]
                print "polarity", self.polarity_value

        self.label = -1
        if self.negative_value < self.positive_value:
            self.label = 1  # positive
        elif self.negative_value > self.positive_value:
            self.label = 0  # negative
        else:
            self.label = 2  # neutral

        insert(review_id, review_name, review_body,
               self.positive_value, self.negative_value,
               self.neutral_value, self.polarity_value, self.label)


def insert(review_id, review_name, review_body, positive, negative, neutral, polarity, label):
    query_plain = review_id + "," + \
                  '"' + review_name + '"' + "," + \
                  '"' + review_body + '"' + "," + \
                  positive + "," + \
                  negative + "," + \
                  neutral + "," + \
                  polarity + "," + \
                  label
    query = "REPLACE INTO " + table_name + " VALUES (" + query_plain + ")"
    cursor.execute(query)
    db.commit()


def do_sentiment_analysis(review_id, review_name, review_body):
    Parser(review_id, review_name, review_body)


def get_last_authorid():
    query = "SELECT authorId FROM sentiment_analysis." + table_name + " order by authorId desc limit 1"
    cursor.execute(query)
    data = cursor.fetchone()
    return data[0]


def run():
    with open(collection, 'rb') as csvfile:
        documents = csv.reader(csvfile, delimiter=' ', quotechar='|')
        index = 0
        last_index = get_last_authorid()
        for row in documents:
            index += 1
            if index < last_index:
                continue
            else:
                # print "index", index
                # print "last_index", last_index
                doc = ' '.join(row)
                doc_array = doc.split(',')
                review_id = doc_array[0]
                review_name = doc_array[3].replace('"', '')
                review_body = doc_array[4].replace('"', '')
                do_sentiment_analysis(review_id, review_name, review_body)


run()

db.close()
