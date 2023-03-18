import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Shoes2Spider(CrawlSpider):
    name            = "shoes2"
    allowed_domains = ["stockx.com"]
    start_urls      = ["https://www.stockx.com/sneakers"]

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths = "//div[@class='css-pnc6ci']/a"), 
            callback                      = "parse_item", 
            follow                        = True
        ),
    )

    def parse_item(self, response):
        
        # def get_xpath(xpath_string):
        #     response.xpath(xpath_string).get(default = "NA").strip()       
        
        #print(response.url)
        
        yield {
              "brand": response.xpath("//h1[@class='chakra-heading css-twoo7s']/text()").get(default = "NA").strip()
            , "name":  response.xpath("//span[@class='chakra-heading css-7ouhme']/text()").get(default = "NA").strip()
            , "last_sale_price": response.xpath("//p[@class='chakra-text css-13uklb6']/text()").get(default = "NA").strip()
            , "last_sale_price_vs_retail_price": response.xpath("//div[@class='css-70qvj9']/p[2]/text()").get(default = "NA").strip()
            , "last_sale_price_vs_retail_price_pct": response.xpath("//div[@class='css-70qvj9']/p[3]/text()").get(default = "NA").strip()
        }
        
        
        # yield {
        #       "brand": get_xpath("//p[@class='chakra-text css-17b7qhr']/text()")
        #     , "name":  get_xpath("//h1[@class='chakra-heading css-twoo7s']/span/text()")
        #     , "last_sale_price": get_xpath("//p[@class='chakra-text css-13uklb6']/text()")
        #     , "last_sale_price_vs_retail_price": get_xpath("//p[@class='chakra-text css-17b7qhr']/text()")
        #     , "last_sale_price_vs_retail_price_pct": get_xpath("//p[@class='chakra-text css-17b7qhr'][2]/text()")
        #     , "url": response.url
        # }


