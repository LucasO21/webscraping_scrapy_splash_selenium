import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as AC


class ExampleSpider(scrapy.Spider):
    name = "example"
    # allowed_domains = ["www.slickdeals.com"]
    # start_urls = ["http://www.slickdeals.com/"]
    
    def start_requests(self):
        yield SeleniumRequest(
            url        = "https://slickdeals.net/computer-deals/",
            wait_time  = 3,
            screenshot = True,
            callback   = self.parse
            
        )

    def parse(self, response):
        # img = response.meta["screenshot"]
        # with open("screenshot.png", "wb") as f:
        #     f.write(img)
            
        # Get drive
        driver = response.meta["driver"]
        
        # Selector object
        html = driver.page_source
        response_obj = Selector(text = html)
        
        # Scroll until the specified element is located
        while True:
            try:
                element = WDW(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@class='bp-c-pagination_right bp-c-button--unstyled bp-c-pagination_next']")))
                
                actions = AC(driver)
                actions.move_to_element(element).perform()
                
                break
            except:
                # Stop scrolling if the element is not found
                break
        
        
        # Click on next page button
        next_page_button = driver.find_element_by_xpath("//button[@class='bp-c-pagination_right bp-c-button--unstyled bp-c-pagination_next']")
        next_page_button.click()
        
        #driver.save_screenshot("screenshot_3.png")
        
        # Extract data
        for product in response_obj.xpath("//li[@class='bp-p-blueberryDealCard bp-p-filterGrid_item bp-p-dealCard bp-c-card']/div[@class='bp-c-card_content']"):
            yield {
                "name": product.xpath(".//a[@class='bp-c-card_title bp-c-link']/text()").get(default = "NA").strip()
            }
