import scrapy


class StatisticsSpider(scrapy.Spider):
    name = "statistics"
    allowed_domains = ["fantasy.premierleague.com"]
    start_urls = ["https://fantasy.premierleague.com/"]

    def parse(self, response):
        for player in response.xpath("//table[@class='Table-ziussd-1 ElementTable-sc-1v08od9-0 dUELIG OZmJL']//tbody//tr"):
            
            yield {
                   "name": player.xpath(".//div[@class='ElementInTable__Name-y9xi40-1 heNyFi']/text()").get()
                ,  "team": player.xpath(".//div[@class='ElementInTable__Info-y9xi40-2 XzKWB']//span[1]/text()").get()
                ,  "pos": player.xpath(".//div[@class='ElementInTable__Info-y9xi40-2 XzKWB']//span[2]/text()").get()
                # "cost": player.xpath().get(),
                # "sel": player.xpath().get(),
                # "form": player.xpath().get(),
                # "points": player.xpath().get(),
                
            }

# "//table[@class='Table-ziussd-1 ElementTable-sc-1v08od9-0 dUELIG OZmJL']//tbody//tr//div[@class='ElementInTable__Name-y9xi40-1 heNyFi']/text()"
# "//table[@class='Table-ziussd-1 ElementTable-sc-1v08od9-0 dUELIG OZmJL']//tbody//tr//div[@class='ElementInTable__Info-y9xi40-2 XzKWB']//span[1]/text()"

