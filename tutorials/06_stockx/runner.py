# imports
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from stockx.spiders.shoes import ShoesSpider


# instantiate process class
process = CrawlerProcess(settings = get_project_settings())
process.crawl(ShoesSpider)
process.start()