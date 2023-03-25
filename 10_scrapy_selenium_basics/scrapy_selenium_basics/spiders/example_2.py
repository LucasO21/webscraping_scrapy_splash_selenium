import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as AC


class Example2Spider(scrapy.Spider):
    name = "example_2"
    allowed_domains = ["www.slickdeals.com"]
    # start_urls = ["http://www.slickdeals.com/"]
    
    # # Override urls
    # def start_requests(self):
    #     yield SeleniumRequest(
    #         url        = "https://slickdeals.net/computer-deals/",
    #         wait_time  = 3,
    #         screenshot = True,
    #         callback   = self.parse
    #     )
    
    # URL
    url = "https://slickdeals.net/computer-deals/?page={}"
    
    # Start requests
    def start_requests(self):
        for i in range(1, 4):
            yield scrapy.Request(self.url.format(i))
    

    # Parse method
    def parse(self, response):
        
        # Extract data from the first page
        for product in response.xpath("//li[@class='bp-p-blueberryDealCard bp-p-filterGrid_item bp-p-dealCard bp-c-card']/div[@class='bp-c-card_content']"):
            yield {
                  "link": response.urljoin(product.xpath(".//a[@class='bp-c-card_title bp-c-link']/@href").get())
                , "name": product.xpath(".//a[@class='bp-c-card_title bp-c-link']/text()").get(default="NA").strip()
                , "current_price": product.xpath(".//span[@class='bp-p-dealCard_price']/text()").get(default="NA").strip()
                , "normal_price": product.xpath(".//span[@class='bp-p-dealCard_originalPrice']/text()").get(default="NA").strip()
                , "store": product.xpath(".//span[@class='bp-c-card_subtitle']/text()").get(default="NA").strip()
                , "posted_day": product.xpath(".//span[@class='bp-p-blueberryDealCard_timestamp']/text()").get(default="NA").strip()
                #, "seller": product.xpath(".//span[@class='bp-p-blueberryDealCard_timestamp']/text()[not(contains(., '\n'))]").get(default="NA").strip()
                
            }
   
