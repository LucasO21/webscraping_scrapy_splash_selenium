# Libraries ----
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Spider Class ----
class BikesSpider(scrapy.Spider):
    name = "bikes"
    allowed_domains = ["www.cannondale.com"]
    start_urls = ["https://www.cannondale.com/en-us/bikes/"]


    # Driver init
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        # Wait for the necessary elements to load correctly
        self.driver.implicitly_wait(10)  # Adjust the wait time as necessary for the page to load

        # Use Selenium's page source to create a Selector
        resp = Selector(text=self.driver.page_source)

        # Extract all links from the specified divs
        for product_card in resp.xpath("//div[contains(@class, 'product-card card filter-and-sort__product -has-3Q')]"):
            link = product_card.xpath(".//a/@href").get()
            if link:
                #yield scrapy.Request(response.urljoin(link), callback=self.parse_details)
                yield {'href': response.urljoin(link)}

    def parse_details(self, response):
        # Detailed parsing logic here
        pass