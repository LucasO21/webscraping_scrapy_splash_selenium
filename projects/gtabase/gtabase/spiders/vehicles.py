# # Packages        
# import scrapy
# from scrapy_selenium import SeleniumRequest
# from scrapy.selector import Selector
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait as WDW
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains as AC
# from webdriver_manager.chrome import ChromeDriverManager
# import itertools
# import time


# # Spider Method
# class VehiclesSpider(scrapy.Spider):
#     name = "vehicles"
#     allowed_domains = ["gtabase.com"]
#     start_urls = ["https://www.gtabase.com/grand-theft-auto-v/vehicles/#sort=attr.ct3.frontend_value&sortdir=desc&page=1"]
    
#     # Initialize Counter
#     # counter = 0

#      # Driver Init
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         chrome_options = Options()
#         chrome_options.add_argument("--headless")
#         self.driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
        
        
#      # Parse Method (Get Links)
#     def parse(self, response):
#         self.driver.get(response.url)
        
#         # Scroll Till The Middle of the Page
#         viewport_height = self.driver.execute_script("return Math.max(document.documentElement.clientHeight, window.innerHeight || 0);")
#         self.driver.execute_script(f"window.scrollTo(0, {viewport_height/2});")
        
#         # Store Response
#         resp = Selector(text=self.driver.page_source)
        
#         # Extract Links
#         for i, vehicle_card in itertools.islice(enumerate(resp.xpath("//div[contains(@class, 'product') and contains(@class, 'item') and contains(@class, 'ln-element')]")), 4): # Testing With 3 Links
#         #for vehicle_card in resp.xpath("//div[contains(@class, 'product') and contains(@class, 'item') and contains(@class, 'ln-element')]"):        
#             link = response.urljoin(vehicle_card.xpath(".//a[contains(@class, 'product') and contains(@class, 'item-link')]/@href").get())
#             yield scrapy.Request(link, callback = self.parse_details)
             
#     # Extract Vehicle Details
#     def parse_details(self, response):
        
#         # Open URL
#         self.driver.get(response.url)
        
#         # Extract Data
#         for vehicle_info in response.xpath("//div[@class='article-content']"):
#             name = response.xpath(".//h2[5]/text()").get(default = "NA").strip()
#             manufacturer = response.xpath(".//dl/dd//span//a[contains(@title, 'Vehicle Class')]/text()").get(default = "NA").strip()
#             # acquisition = response.xpath(".//dl/dd//span//a[contains(@title, 'Acquisition')]/text()").get(default = "NA").strip()
#             # price = response.xpath(".//dl/dd//span[text()='GTA Online Price']/following-sibling::span/text()").get(default = "NA").strip()
#             # storage = response.xpath(".//dl/dd//span//a[contains(@title, 'Storage Location')]/text()").get(default = "NA").strip()
        
#             yield {
#                 "name": name
#                 , "manufacturer": manufacturer
#                 # , "acquisition": acquisition
#                 # , "price": price
#                 # , "storage": storage
#             }            
            
            
#             # # Increment Counter / Check if Counter is <= 3
#             # self.counter += 1
#             # if self.counter < 3:

#     #         # Get Next Page URL & Callback parse_details
#     #         next_page = response.xpath("(//a[@title='Next'])[2]/@href").get()
#     #         if next_page:
#     #             absolute_url = f"https://www.gtabase.com/grand-theft-auto-v/vehicles/{next_page}"
#     #             yield SeleniumRequest(
#     #                 url = absolute_url,
#     #                 wait_time = 5,
#     #                 callback = self.parse_details
#     #             )
#     #         # else:
#     #         #     self.log("REACHED PAGE LIMIT, SPIDER STOPPED")
        
#     # Close Spider    
#     def spider_closed(self, reason):
#         self.driver.quit()

         
# REPREX -----------
# Packages        
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as AC
from webdriver_manager.chrome import ChromeDriverManager
import itertools
import time


# Spider Method
class VehiclesSpider(scrapy.Spider):
    name = "vehicles"
    allowed_domains = ["gtabase.com"]
    start_urls = ["https://www.gtabase.com/grand-theft-auto-v/vehicles/#sort=attr.ct3.frontend_value&sortdir=desc&page=1"]
    
    # Initialize Counter
    counter = 0

     # Driver Init
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
        
        
     # Parse Method (Get Links)
    def parse(self, response):
        self.driver.get(response.url)
        
        # Scroll Till The Middle of the Page
        viewport_height = self.driver.execute_script("return Math.max(document.documentElement.clientHeight, window.innerHeight || 0);")
        self.driver.execute_script(f"window.scrollTo(0, {viewport_height/2});")
        
        # Store Response
        resp = Selector(text=self.driver.page_source)
        
        # Extract Links
        for i, vehicle_card in itertools.islice(enumerate(resp.xpath("//div[contains(@class, 'product') and contains(@class, 'item') and contains(@class, 'ln-element')]")), 4): # Testing With 4 Links       
            link = response.urljoin(vehicle_card.xpath(".//a[contains(@class, 'product') and contains(@class, 'item-link')]/@href").get())
            yield scrapy.Request(link, callback = self.parse_details)
             
    # Extract Vehicle Details
    def parse_details(self, response):
        
        # Open URL
        self.driver.get(response.url)
        
        # Extract Data
        for vehicle_info in response.xpath("//div[@class='article-content']"):
            name = response.xpath(".//h2[5]/text()").get(default = "NA").strip()
            manufacturer = response.xpath(".//dl/dd//span//a[contains(@title, 'Vehicle Class')]/text()").get(default = "NA").strip()
        
            yield {
                  "name": name
                , "manufacturer": manufacturer
            }            
            
            
        # Increment Counter / Check if Counter is <= 3
        self.counter += 1
        if self.counter < 4:

        # Get Next Page URL & Callback parse_details
            next_page = response.xpath("(//a[@title='Next'])[2]/@href").get()
            if next_page:
                absolute_url = f"https://www.gtabase.com/grand-theft-auto-v/vehicles/{next_page}"
                yield SeleniumRequest(
                    url = absolute_url,
                    wait_time = 5,
                    callback = self.parse_details
                )
            else:
                self.log("REACHED PAGE LIMIT, SPIDER STOPPED")
        
    # Close Spider    
    def spider_closed(self, reason):
        self.driver.quit()

         
     