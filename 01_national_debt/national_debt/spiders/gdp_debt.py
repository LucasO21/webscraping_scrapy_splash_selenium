import scrapy


class GdpDebtSpider(scrapy.Spider):
    name = "gdp_debt"
    allowed_domains = ["worldpopulationreview.com"]
    start_urls = ["http://worldpopulationreview.com/country-rankings/countries-by-national-debt"]

    def parse(self, response):
        rows = response.xpath("(//table)[2]/tbody/tr")
        for row in rows:
            yield {
                'country_name': row.xpath(".//td[1]/a/text()").get(),
                'year': row.xpath(".//td[2]/text()").get(),
                'debt_dollars': row.xpath(".//td[3]/text()").get(),
                'gdp_debt': row.xpath(".//td[4]/text()").get()
            }
    
    # def parse(self, response):
    #     rows = response.xpath("//table/tbody/tr")
    #     for row in rows:
    #         yield {
    #             'country_name': row.xpath(".//td[1]/a/text()").get(),
    #             'gdp_debt': row.xpath(".//td[2]/text()").get()
    #         }
