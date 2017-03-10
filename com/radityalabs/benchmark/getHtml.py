import requests

url = 'http://text-processing.com/demo/sentiment/'
payload = {'language': 'english', 'text': "bad person"}
r = requests.post(url, data=payload)
print r.url
print r.text

# parser = Parser()
# parser.feed('<html><head><title>Test</title></head>'
#            '<body><h1>Parse me!</h1></body></html>')


# def crawling(response):
#    for quote in response.css("div.quote"):
#        yield {
#            'text': quote.css("span.text::text").extract_first(),
#            'author': quote.css("small.author::text").extract_first(),
#            'tags': quote.css("div.tags > a.tag::text").extract()
#        }

#    next_page_url = response.css("li.next > a::attr(href)").extract_first()
#    if next_page_url is not None:
#        yield scrapy.Request(response.urljoin(next_page_url))

import mysql.connector
import csv
import requests
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup

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
        self.review_id = review_id
        self.review_name = reviewName
        self.review_body = review_body
        print "id", review_id
        print "reviewName", review_name
        print "reviewBody", review_body

        # HTMLParser.__init__(self)
        # self.feed(self.request.text)
        payload = {'language': 'english', 'text': review_body}
        self.request = requests.post(url, data=payload)
        self.html = BeautifulSoup(self.request.text)
        # print parsed_html.body.find('div', attrs={'class': 'container'}).text
        self.sentiment_collection = self.html.body.find('div', attrs={'class': 'span-9 last'})
        self.collection_sentiment = self.sentiment_collection.findAll('li')
        for item in self.collection_sentiment:
            self.sentiment_result = item.text
            print self.sentiment_result

        #self.num_of_collection = len(self.collection_sentiment)
        #print self.num_of_collection

        # print self.html

    def handle_data(self, data):
        if "pos:" in data:
            positive = data.split(None)
            val_pos = positive[1]
            insert(self.review_id, self.reviewName, self.review_body, val_pos, 0, 0, 0)
            print "positive", positive[1]
        if "neg:" in data:
            negative = data.split(None)
            print "negative", negative[1]
        if "neutral:" in data:
            neutral = data.split(None)
            print "neutral", neutral[1]
        if "polar:" in data:
            polarity = data.split(None)
            print "polarity", polarity[1]


def insert(review_id, review_name, review_body, positive, negative, neutral, polarity):
    query = "INSERT OR UPDATE INTO " + table_name + " VALUES (" + query_plain + ")"
    cursor.execute(query)
    db.commit()


def do_sentiment_analysis(review_id, review_name, review_body):
    Parser(review_id, review_name, review_body)


with open(collection, 'rb') as csvfile:
    documents = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in documents:
        doc = ' '.join(row)
        doc_array = doc.split(',')
        reviewId = doc_array[0]
        reviewName = doc_array[3]
        reviewBody = doc_array[4].replace('"', '')
        do_sentiment_analysis(reviewId, reviewName, reviewBody)

db.close()
