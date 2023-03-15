import scrapy


class ArticlesSpider(scrapy.Spider):
    
    name = "articles"
    allowed_domains = ["www.techcrunch.com"]
    start_urls = ["https://techcrunch.com/category/apps"]

    def parse(self, response):
        for post in response.xpath("////div[@class='post-block post-block--image post-block--unread']"):
            
            title  = post.xpath(".//a[@class='post-block__title__link']/text()").get().strip()
            date   = post.xpath(".//div[@class='river-byline']/time/text()").get().strip()
            author = post.xpath(".//span[@class='river-byline__authors']/a/text()").get().strip()
            link   = post.xpath(".//a[@class='post-block__title__link']/@href").get().strip()
            
            yield {
                "title":  title,
                "date":   date,
                "author": author,
                "link":   link
            }
