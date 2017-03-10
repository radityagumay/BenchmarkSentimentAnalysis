from HTMLParser import HTMLParser
import scrapy
import requests

url = 'http://text-processing.com/demo/sentiment/'
payload = {'language': 'english', 'text': "bad person"}
r = requests.post(url, data=payload)
print r.url
print r.text


class Parser(HTMLParser):
    #    def handle_starttag(self, tag, attrs):
    # print "Encountered a start tag:", tag
    # print "Start tag:", tag
    # for attr in attrs:
    #    print "     attr:", attr

    # def handle_endtag(self, tag):
    #    print "Encountered an end tag :", tag

    def handle_data(self, data):
        #print "Encountered some data  :", data
        if "pos" in data:
            print data
        if "neg" in data:
            print data
        if "polar" in data:
            print data
        if "neutral" in data:
            print data


parser = Parser()
parser.feed(r.text)
