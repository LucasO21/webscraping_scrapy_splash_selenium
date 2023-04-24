# # Spider Method
# class Vehicles2Spider(scrapy.Spider):
#     name = "vehicles2"
#     allowed_domains = ["gtabase.com"]
#     start_urls = [
#         "https://www.gtabase.com/grand-theft-auto-v/vehicles/#sort=attr.ct3.frontend_value&sortdir=desc&page=2"
#     ]

#     # Driver Init
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         chrome_options = Options()
#         chrome_options.add_argument("--headless")
#         self.driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
        
#     # Parse Method (Get Links)
#     def parse(self, response):
#         self.driver.get(response.url)
        
#         # Scroll Till The Middle of the Page
#         viewport_height = self.driver.execute_script("return Math.max(document.documentElement.clientHeight, window.innerHeight || 0);")
#         self.driver.execute_script(f"window.scrollTo(0, {viewport_height/2});")
        
#         # Store Response
#         resp = Selector(text = self.driver.page_source)
#         # resp = HtmlResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')

        
#         # Extract Links
#         for i, vehicle_card in itertools.islice(enumerate(resp.xpath("//div[contains(@class, 'product') and contains(@class, 'item') and contains(@class, 'ln-element')]")), 4): # Testing With 4 Links       
#             link = response.urljoin(vehicle_card.xpath(".//a[contains(@class, 'product') and contains(@class, 'item-link')]/@href").get())
#             yield scrapy.Request(url = link, callback = self.parse_details)
             
#     # Extract Vehicle Details
#     def parse_details(self, response):
        
#         # Open URL
#         sel = Selector(text = response.body)
        
#         # Extract Data
#         for vehicle_info in sel.xpath("//div[@class='article-content']"):
#             name = vehicle_info.xpath(".//h2[5]/text()").get(default = "NA").strip()
#             manufacturer = vehicle_info.xpath(".//dl/dd//span//a[contains(@title, 'Vehicle Class')]/text()").get(default = "NA").strip()
        
#             yield {
#                 "name": name,
#                 "manufacturer": manufacturer
#             }            
            
            
#         # # Increment Counter / Check if Counter is <= 3
#         # self.counter += 1
#         # if self.counter < 4:

#         # Get Next Page URL & Callback parse_details
#         # next_page = response.xpath("(//a[@title='Next'])[2]/@href").get()
#         # if next_page:
#         #     absolute_url = f"https://www.gtabase.com/grand-theft-auto-v/vehicles/{next_page}"
#         #     absolute_url = re.sub(r"#", r"?", absolute_url)
#         #     yield SeleniumRequest(
#         #         url = absolute_url,
#         #         wait_time = 5,
#         #         callback = self.parse_details
#         #     )
#         # else:
#         #     self.log("REACHED PAGE LIMIT, SPIDER STOPPED")
        
#     # Close Spider    
#     def spider_closed(self, reason):
#         self.driver.quit()




# ######### SPIDER 2

# import scrapy
# from scrapy.selector import Selector
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys


# # # # Spider Method
# class Vehicles2Spider(scrapy.Spider):
#     name = "vehicles2"
#     allowed_domains = ["gtabase.com"]
#     #start_urls = ["https://www.gtabase.com/grand-theft-auto-v/vehicles/#sort=attr.ct3.frontend_value&sortdir=desc&page=2"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         chrome_options = Options()
#         chrome_options.add_argument("--headless")
#         self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        
#     def start_requests(self):                  
#         yield SeleniumRequest(
#             url = "https://www.gtabase.com/grand-theft-auto-v/vehicles/#sort=attr.ct3.frontend_value&sortdir=desc",
#             wait_time = 3,
#             callback = self.parse
#         )

#     def parse(self, response):
        
#         for i, vehicle_card in itertools.islice(enumerate(response.xpath("//div[contains(@class, 'product') and contains(@class, 'item') and contains(@class, 'ln-element')]")), 4): # Testing With 4 Links
#             link = response.urljoin(vehicle_card.xpath(".//a[contains(@class, 'product') and contains(@class, 'item-link')]/@href").get())
#             #yield scrapy.Request(url=link, callback=self.parse_item)
#             yield {"link": link}
            
#     # def parse_item(self, response):
#     #     sel = Selector(text=response.body)
        
#     #     for vehicle_info in sel.xpath("//div[@class='article-content']"):
#     #         name = vehicle_info.xpath(".//h2[5]/text()").get(default = "NA").strip()
#     #         manufacturer = vehicle_info.xpath(".//dl/dd//span//a[contains(@title, 'Vehicle Class')]/text()").get(default = "NA").strip()           
        
#     #         yield {
#     #             "name": name,
#     #             "manufacturer": manufacturer
#     #         }     

        
        
#         # Get Next Page URL & Callback parse_details        
#         next_page = response.xpath("//li[@class='item pages-item-next']/a['data-value']").get()
#         #next_page = int(next_page)
            
#         if next_page == "2":
#             next_page_url = f"https://www.gtabase.com/grand-theft-auto-v/vehicles/#sort=attr.ct3.frontend_value&sortdir=desc&page={next_page}"
#             yield SeleniumRequest(
#                 url = next_page_url,
#                 wait_time = 5,
#                 callback = self._parse
#             )
        
# #         # next_page_disabled = response.xpath("//li[contains(@class, 'item') and contains(@class, 'pages-item-next') and contains(@class, 'disabled')]")        
# #         # if not next_page_disabled:
# #         #     #page += 1
# #         #     #absolute_url = "https://www.gtabase.com/grand-theft-auto-v/vehicles/#sort=attr.ct3.frontend_value&sortdir=desc&page={}".format(page)
# #         #     absolute_url = "https://www.gtabase.com/grand-theft-auto-v/vehicles/#sort=attr.ct3.frontend_value&sortdir=desc&page=2"
# #         #     yield SeleniumRequest(
# #         #         url=absolute_url,
# #         #         wait_time=5,
# #         #         callback=self.start_requests
# #         #     )
            
# #     # Close Spider    
#     def spider_closed(self, reason):
#         self.driver.quit()


# ######### SPIDER 3

# import scrapy
# from scrapy.selector import Selector
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys


# # # Spider Method
# class Vehicles2Spider(scrapy.Spider):
#     name = "vehicles2"
#     allowed_domains = ["gtabase.com"]
#     start_urls = [
#         "https://www.gtabase.com/grand-theft-auto-v/vehicles/?sort=attr.ct3.frontend_value&sortdir=desc&page=1",
#         "https://www.gtabase.com/grand-theft-auto-v/vehicles/?sort=attr.ct3.frontend_value&sortdir=desc&page=2"
#     ]

#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #     chrome_options = Options()
#     #     chrome_options.add_argument("--headless")
#     #     self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        
#     def start_requests(self):            
#         for url in self.start_urls:      
#             yield SeleniumRequest(
#                 url = url,
#                 wait_time = 3,
#                 callback = self.parse
#             )

#     def parse(self, response):
        
#         for i, vehicle_card in itertools.islice(enumerate(response.xpath("//div[contains(@class, 'product') and contains(@class, 'item') and contains(@class, 'ln-element')]")), 4): # Testing With 4 Links
#             link = response.urljoin(vehicle_card.xpath(".//a[contains(@class, 'product') and contains(@class, 'item-link')]/@href").get())
#             #yield scrapy.Request(url=link, callback=self.parse_item)
#             yield {"link": link}
            
#     # def parse_item(self, response):
#     #     sel = Selector(text=response.body)
        
#     #     for vehicle_info in sel.xpath("//div[@class='article-content']"):
#     #         name = vehicle_info.xpath(".//h2[5]/text()").get(default = "NA").strip()
#     #         manufacturer = vehicle_info.xpath(".//dl/dd//span//a[contains(@title, 'Vehicle Class')]/text()").get(default = "NA").strip()
        
#     #         yield {
#     #             "name": name,
#     #             "manufacturer": manufacturer
#     #         }       
        
        
#         # Get Next Page URL & Callback parse_details        
#         # next_page = response.xpath("//li[@class='item pages-item-next']/a['data-value']").get()
#         # #next_page = int(next_page)
            
#         # if next_page == "2":
#         #     next_page_url = f"https://www.gtabase.com/grand-theft-auto-v/vehicles/#sort=attr.ct3.frontend_value&sortdir=desc&page={next_page}"
#         #     yield SeleniumRequest(
#         #         url = next_page_url,
#         #         wait_time = 5,
#         #         callback = self._parse
#         #   )
        
#         # next_page_disabled = response.xpath("//li[contains(@class, 'item') and contains(@class, 'pages-item-next') and contains(@class, 'disabled')]")        
#         # if not next_page_disabled:
#         #     #page += 1
#         #     #absolute_url = "https://www.gtabase.com/grand-theft-auto-v/vehicles/#sort=attr.ct3.frontend_value&sortdir=desc&page={}".format(page)
#         #     absolute_url = "https://www.gtabase.com/grand-theft-auto-v/vehicles/#sort=attr.ct3.frontend_value&sortdir=desc&page=2"
#         #     yield SeleniumRequest(
#         #         url=absolute_url,
#         #         wait_time=5,
#         #         callback=self.start_requests
#         #     )
            
#     # Close Spider    
#     def spider_closed(self, reason):
#         self.driver.quit()