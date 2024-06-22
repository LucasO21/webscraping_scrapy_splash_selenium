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
import itertools
import time
import re
import logging

# Spider Method
class MlplatformsSpider(scrapy.Spider):
    name            = "mlplatforms"
    allowed_domains = ["www.g2.com"]
    start_urls      = ["https://www.g2.com/categories/data-science-and-machine-learning-platforms/"]

    # Init Method
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        
    # Parse Method
    def parse(self, response, **kwargs):
        
        # Get Driver
        self.driver.get(response.url)
        
        # Store response    
        resp = Selector(text=self.driver.page_source)
        
        # Extract Links
        for pcard in resp.xpath("//div[contains(@class, 'product-card x-ordered-events-initialized')]"):
            link = pcard.xpath(".//a[@class='d-ib c-midnight-100 js-log-click']/@href")
            
            yield {
                "link": link
            }
            

