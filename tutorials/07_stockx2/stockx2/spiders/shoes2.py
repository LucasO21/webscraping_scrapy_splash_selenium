import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Shoes2Spider(CrawlSpider):
    name            = "shoes2"
    allowed_domains = ["stockx.com"]
    #start_urls      = ["https://www.stockx.com/sneakers"]

    
    # user agent override
    user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"    
    
    def start_requests(self):
        yield scrapy.Request(
            url     = "https://www.stockx.com/sneakers",
            headers = {"User-Agent": self.user_agent}
        )    
        
    rules = (
        Rule(
            LinkExtractor(restrict_xpaths = "//div[@class='css-pnc6ci']/a"), 
            callback                      = "parse_item", 
            follow                        = True,
            process_request               = "set_user_agent"
        ),       
        
        # Rule(
        #     LinkExtractor(restrict_xpaths = "//a[@aria-label='Next']"),
        #     follow                        = True,
        #     process_request               = "set_user_agent"            
        # )
    )
    
    def set_user_agent(self, request, spider):
        request.headers["User-Agent"] = self.user_agent
        return request

    def parse_item(self, response):     
        
        #print(response.url)
        
        yield {
              "brand": response.xpath("//h1[@class='chakra-heading css-twoo7s']/text()").get(default = "NA").strip()
            , "name":  response.xpath("//span[@class='chakra-heading css-7ouhme']/text()").get(default = "NA").strip()
            , "last_sale_price": response.xpath("//p[@class='chakra-text css-13uklb6']/text()").get(default = "NA").strip()
            , "last_sale_price_vs_retail_price": response.xpath("//div[@class='css-70qvj9']/p[2]/text()").get(default = "NA").strip()
            , "last_sale_price_vs_retail_price_pct": response.xpath("//div[@class='css-70qvj9']/p[3]/text()").get(default = "NA").strip()
            , "user-agent": response.request.headers.get("User-Agent").decode('utf-8')
        }
        
        
      

