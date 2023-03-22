import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


class StocklistSelSpider(scrapy.Spider):
    name            = "stocklist_sel"
    allowed_domains = ["www.tradingview.com"]
    start_urls      = ["https://www.tradingview.com/markets/stocks-usa/sectorandindustry-industry/"]
    
    
    # Constructor
    def __init__(self):
        
        # Chrome driver setup
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        
        # Chrome driver url
        driver = webdriver.Chrome(ChromeDriverManager().install())
        url    = "https://www.tradingview.com/markets/stocks-usa/sectorandindustry-industry/"
        driver.get(url)
        
        # Load more xpath
        load_more_xpath  = "//button[@class='loadButton-Hg5JK_G3']"
        load_more_botton = driver.find_element_by_xpath(load_more_xpath)
        
        # Scroll until the specified element is located
        while True:
            try:
                element = WDW(driver, 10).until(EC.visibility_of_element_located((By.XPATH, load_more_xpath)))
                
                actions = AC(driver)
                actions.move_to_element(element).perform()
                
                break
            except:
                # Stop scrolling if the element is not found
                break

        # Click on the element
        load_more_botton.click()
        time.sleep(3)
        
        
        
        # Store html markup
        self.html = driver.page_source
        
        
        # Close driver
        driver.close()
        
        
    # Parse 
    def parse(self, response):
        resp = Selector(text = self.html)
        
        for stock in resp.xpath("//tr[@class='row-EdyDtqqh listRow']"):
            
            yield {
                "link": response.urljoin(stock.xpath(".//td[@class='cell-TKkxf89L left-TKkxf89L cell-fixed-f5et_Mwd onscroll-shadow']/a/@href").get())
            }
