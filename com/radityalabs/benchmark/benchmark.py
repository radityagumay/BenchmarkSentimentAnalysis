from HTMLParser import HTMLParser
import requests


url = 'http://text-processing.com/demo/sentiment/'
payload = {'language': 'english', 'text': "Still auto refreshes, scrolls to top on it's own, so annoying! "}
r = requests.post(url, data=payload)
s = r.text

print "Url", r.url
print "Html Response", s


class Parser(HTMLParser):
    def handle_data(self, data):
        if "pos:" in data:
            print data
        if "neg:" in data:
            print data
        if "polar:" in data:
            print data
        if "neutral:" in data:
            print data


parser = Parser()
parser.feed(s)
