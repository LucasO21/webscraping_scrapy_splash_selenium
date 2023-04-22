import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class ShoesSpider(scrapy.Spider):
    name = 'shoes'
    start_urls = ['https://stockx.com/sneakers?page=1']

    def __init__(self, *args, **kwargs):
        super(ShoesSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                wait_time=10,
                callback=self.parse,
                dont_filter=True,
                service=self.service,
                options=self.options
            )

    def parse(self, response):
        for div in response.xpath('//div[@class="css-pnc6ci"]'):
            link = div.xpath('.//a/@href')[0]
            yield SeleniumRequest(
                url=response.urljoin(link.get()),
                wait_time=10,
                callback=self.parse_shoe,
                dont_filter=True,
                service=self.service,
                options=self.options
            )

    def parse_shoe(self, response):
        driver = response.request.meta['driver']
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[@class='chakra-heading css-twoo7s']")))
        yield {
            'href': response.url,
            'name': driver.find_element(By.XPATH, "//h1[@class='chakra-heading css-twoo7s']"),
        }
