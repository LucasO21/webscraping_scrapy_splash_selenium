import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TopMoviesSpider(CrawlSpider):
    name            = "top_movies"
    allowed_domains = ["imdb.com"]
    start_urls      = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//td[@class='titleColumn']"), callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        print(response.url)
