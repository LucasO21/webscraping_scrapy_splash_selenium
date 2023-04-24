# PAGINATION WITH NEXT PAGE LINK

import scrapy
import scraper_helper


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": scraper_helper.headers()
    }

    def parse(self, response):
        
        # current page
        print(response.xpath("//li[@class='current']/text()").get())
        
        # next button
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        
        yield scrapy.Request(response.urljoin(next_link), callback = self.parse)
