# VEHICLES SPIDER WITH SCRAPY SELENIUM AND BEAUTIFUL SOUP

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
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.http import HtmlResponse
import itertools
import time
import re
from bs4 import BeautifulSoup


# # Spider Method
class Vehicles2Spider(scrapy.Spider):
    name = "vehicles2"
    allowed_domains = ["gtabase.com"]
    start_urls = ["https://www.gtabase.com/grand-theft-auto-v/vehicles/#sort=attr.ct3.frontend_value&sortdir=desc"]

    # Init Method
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    # Start Request Method
    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SeleniumRequest(
    #             url=url,
    #             wait_time=3,
    #             callback=self.parse
    #         )

    # Parse Method
    def parse(self, response):
        
        # Get Driver
        self.driver.get(response.url)
        
        # Start Loop
        while True:
            try:
                # - Grab HTML
                soup = BeautifulSoup(self.driver.page_source, 'lxml')

                # - Grab links
                posting_card = soup.find_all('div', class_=lambda x: x and x.startswith('item_'))

                # - Extract Vehicle Card
                links = [card.find('a', class_='product-item-link')['href'] for card in soup.find_all('div', class_ = lambda x: x and x.startswith('item_'))]
                links = ["https://www.gtabase.com/" + i for i in links]
                links = links[:3]
                    
                # - Yield Link
                # yield {"link": link} # - Testing
                for link in links:
                    yield SeleniumRequest(url = link, callback = self.parse_items)                

                # - Check If Next Page Xpath is Disabled. If Disabled Then Break. If Not Disabled, Click On Next Page Xpath
                if self.driver.find_elements("xpath", "//li[contains(@class, 'pages-item-next') and contains(@class, 'disabled')]"):
                    break
                else:
                    try:
                        next_button = self.driver.find_element("xpath", "//a[@class='page action next']")
                        next_button.click()
                        WDW(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'product') and contains(@class, 'item') and contains(@class, 'ln-element')]")))     
                    except:
                        break         

            # Exception Handling
            except Exception as e:
                self.logger.error(f"Error: {e}")
                # Handle the exception appropriately
    
    # Parse Items Method
    def parse_items(self, response):
        
        # Open URL
        self.driver.get(response.url)
        
        # Store Response
        resp = Selector(text = self.driver.page_source)
        
        # Extract Items
        for vehicle_info in resp.xpath("//div[@class='article-content']"):
            name = vehicle_info.xpath(".//h2[5]/text()").get(default = "NA").strip()
            manufacturer = vehicle_info.xpath(".//dl/dd//span//a[contains(@title, 'Vehicle Class')]/text()").get(default = "NA").strip()
        
            yield {
                  "name": name,
                  "manufacturer": manufacturer
            }   
        

    # Close Spider
    def spider_closed(self, reason):
        self.driver.quit()
        
        
