import scrapy


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["techcrunch.com"]
    start_urls = ["https://techcrunch.com/category/apps/"]

    def parse(self, response):
        pass
