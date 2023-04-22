import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        
        # current page
        print(response.xpath("//li[@class='current']/text()").get())
        
        # next button
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        
        yield scrapy.Request(response.urljoin(next_link), callback = self.parse)
