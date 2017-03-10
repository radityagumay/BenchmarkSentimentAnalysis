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