# SCRAPY SPIDER
# - 1: Extract links from "https://www.tradingview.com/markets/stocks-usa/sectorandindustry-industry/"
# - 2: Follow each link
# - 3: Extract additional data point on stock details
    
# Packages        
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as AC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import json

# Spider class
class StocklistSelSpider(scrapy.Spider):
    name            = "stocklist_sel_2"
    allowed_domains = ["www.tradingview.com"]
    start_urls      = ["https://www.tradingview.com/markets/stocks-usa/sectorandindustry-industry/"]
    
    # Driver init
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    
    # Parse method (get links)    
    def parse(self, response):
        self.driver.get(response.url)
        
        # Scroll to `load more xpath` then click `load more`
        while True:
            try:
                load_more_botton = self.driver.find_element_by_xpath("//button[@class='loadButton-Hg5JK_G3']")
                actions = AC(self.driver)
                actions.move_to_element(load_more_botton).perform()
                load_more_botton.click()
                time.sleep(3)
            except:
                break
        
        # Store response    
        resp = Selector(text=self.driver.page_source)
        
        # Extract all links
        # for stock in resp.xpath("//tr[@class='row-EdyDtqqh listRow']"):
        #     link = response.urljoin(stock.xpath(".//td[@class='cell-TKkxf89L left-TKkxf89L cell-fixed-f5et_Mwd onscroll-shadow']/a/@href").get())
        #     yield scrapy.Request(link, callback=self.parse_details)
        
        # ----
        # Extract links (testing with 3 links)
        count = 0  # counter for number of links extracted
        
        for stock in resp.xpath("//tr[@class='row-EdyDtqqh listRow']"):
            if count >= 2:
                break  # stop processing after the first 3 links
            
            link = response.urljoin(stock.xpath(".//td[@class='cell-TKkxf89L left-TKkxf89L cell-fixed-f5et_Mwd onscroll-shadow']/a/@href").get())
            
            # Visit the link using selenium
            yield scrapy.Request(link, callback = self.parse_details)
            
            count += 1
        # ----
    
    # Extract details method
    def parse_details(self, response):
        
        # Open url
        self.driver.get(response.url)
        
        # Scroll to `load more xpath` then click `load more`
        while True:
            try:
                load_more_botton = self.driver.find_element_by_xpath("//button[@class='loadButton-Hg5JK_G3']")
                actions = AC(self.driver)
                actions.move_to_element(load_more_botton).perform()
                load_more_botton.click()
                time.sleep(3)
            except:
                break
         
        # Extract data    
        industry = self.driver.find_element_by_xpath("//h1[@class='tv-category-header__title-text']").text.strip()
        
        symbols = []
        for symbol in self.driver.find_elements_by_xpath("//a[@class='apply-common-tooltip tickerNameBox-hMpTPJiS tickerName-hMpTPJiS']"):
            symbols.append(symbol.text.strip())        
            
        company_name = []
        for company in self.driver.find_elements_by_xpath( "//sup[@class='apply-common-tooltip tickerDescription-hMpTPJiS']"):
            company_name.append(company.text.strip())      
        
       
        # Yield data
        yield {
              #"link": response.url
             "industry": industry
            , "symbols": symbols
            , "company": company_name
    }
    
    
    
    # Close driver method
    def closed(self, reason):
        self.driver.quit()
        
        
        # # Save Data        
        # field_names = [
        #      "link"
        #     , "industry"
        #     , "symbols"
        # ]
        
        # # Write the scraped data to the output file in the specified format
        # if self.output_format == 'csv':
        #     with open(self.output_file, 'w', newline='') as f:
        #         writer = csv.DictWriter(f, fieldnames=field_names)
        #         writer.writeheader()
        #         for item in self.items:
        #             writer.writerow(item)
        # elif self.output_format == 'json':
        #     with open(self.output_file, 'w') as f:
        #         json.dump(self.items, f)
