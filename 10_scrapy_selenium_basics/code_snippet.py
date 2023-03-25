
# ## SAMPLE CODE SNIPPET FOR SCRAPY & SELENIUM SPIDER

# import scrapy
# from scrapy_selenium import SeleniumRequest
# from scrapy.selector import Selector
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait as WDW
# from selenium.webdriver.common.by import By

# class Example2Spider(scrapy.Spider):
#     name = "example_2"
#     # allowed_domains = ["www.slickdeals.com"]
#     # start_urls = ["http://www.slickdeals.com/"]

#     # Override urls
#     def start_requests(self):
#         yield SeleniumRequest(
#             url        = "https://slickdeals.net/computer-deals/",
#             wait_time  = 3,
#             screenshot = True,
#             callback   = self.parse
#         )

#     # Parse method
#     def parse(self, response):
        
#         # Get driver
#         driver = response.meta["driver"]
        
#         # Selector object
#         response_obj = Selector(text = driver.page_source)
        
#         # Scroll to the bottom of the page
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
#         # Extract data from the first page
#         for product in response_obj.xpath("//li[@class='bp-p-blueberryDealCard bp-p-filterGrid_item bp-p-dealCard bp-c-card']/div[@class='bp-c-card_content']"):
#             yield {
#                 "name": product.xpath(".//a[@class='bp-c-card_title bp-c-link']/text()").get(default="NA").strip(),
#                 "url": product.xpath(".//a[@class='bp-c-card_title bp-c-link']/@href").get(),
#             }
            
#         count = 0
        
#         while count < 3:        
        
#             # Click on next page button
#             next_page_button = driver.find_element_by_xpath("//button[@class='bp-c-pagination_right bp-c-button--unstyled bp-c-pagination_next']")
#             next_page_button.click()
            
#             # Wait for the page to load
#             WDW(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li[@class='bp-p-blueberryDealCard bp-p-filterGrid_item bp-p-dealCard bp-c-card']/div[@class='bp-c-card_content']")))
            
#             # Update the URL of the SeleniumRequest object to point to the next page
#             next_page_url = driver.current_url
#             yield SeleniumRequest(
#                 url        = next_page_url,
#                 wait_time  = 3,
#                 screenshot = True,
#                   callback   = self.parse
#             )
        
#             count += 1
