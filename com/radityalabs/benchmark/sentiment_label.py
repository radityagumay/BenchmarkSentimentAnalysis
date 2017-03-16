from BeautifulSoup import BeautifulSoup
import mysql.connector
import csv
import requests
import sys
import unicodedata

# for large load data
reload(sys)
sys.setdefaultencoding('utf8')
csv.field_size_limit(500 * 1024 * 1024)

# init connection
database = mysql.connector.connect(
    user='root', password='',
    host='127.0.0.1',
    database='sentiment_analysis'
)

cursor = database.cursor()

table_name = "review_label_benchmark"
csv_name = "csv/collection-csv.csv"
url = "http://text-processing.com/api/sentiment/"


def request_api(authorId, authorName, googleId, reviewBody):
    payload = {'language': 'english', 'text': reviewBody}
    try:
        request = requests.post(url, data=payload)
    except requests.exceptions.RequestException as e:
        print "run service again", e
        print run()
        return

    request.raise_for_status()
    probability = request.json()['probability']
    label = request.json()['label']
    negative = probability['neg']
    positive = probability['pos']
    neutral = probability['neutral']

    if "reviewId" in googleId:
        cleanId = googleId
    else:
        obj = googleId.split('id=')
        cleanId = obj[1]

    query_plain = authorId + "," + \
                  "'" + authorName + "'" + "," + \
                  "'" + cleanId + "'" + "," + \
                  "'" + reviewBody + "'" + "," + \
                  str(positive) + "," + \
                  str(negative) + "," + \
                  str(neutral) + "," + \
                  "'" + label.decode('iso-8859-1').encode('utf-8') + "'"

    print query_plain
    query = "REPLACE INTO " + table_name + " VALUES (" + query_plain + ")"
    try:
        cursor.execute(query)
        database.commit()
    except:
        database.rollback()


def get_last_authorid():
    query = "SELECT authorId FROM sentiment_analysis." + table_name + " order by authorId desc limit 1"
    cursor.execute(query)
    data = cursor.fetchone()
    return data[0] + 1


def is_blank(myString):
    if myString and myString.strip():
        return False
    return True


def run():
    with open(csv_name, 'rU') as csvfile:
        documents = csv.reader(csvfile)
        index = 0
        last_index = get_last_authorid()
        print "last index", last_index
        for row in documents:
            index += 1
            if index < last_index:
                continue
            else:
                doc = '[===]'.join(row)
                doc_array = doc.split('[===]')
                review_id = doc_array[0]
                review_google_id = doc_array[2]
                review_name = doc_array[3].replace('"', '').replace(",", "").replace('\'', '')
                is_empty = is_blank(doc_array[4])
                if is_empty:
                    review_body = "no review consist"
                else:
                    review_body = doc_array[4].replace('"', '').replace(",", "").replace('\'', '')

                request_api(review_id, review_name, review_google_id, review_body)


run()
