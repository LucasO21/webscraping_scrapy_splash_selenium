import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/api/quotes?page=1"]

    def parse(self, response):
        resp = json.loads(response.body)
        quotes = resp.get("quotes")
        
        for quote in quotes:
            yield {
                "author": quote.get("author").get("name"),
                "tags": quote.get("tags"),
                "quotes_test": quote.get("text")
                
            }
