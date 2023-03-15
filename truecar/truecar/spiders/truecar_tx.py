import scrapy


class TruecarTxSpider(scrapy.Spider):
    name = "truecar_tx"
    allowed_domains = ["www.military.truecar.com"]
    start_urls = ["https://military.truecar.com/used-cars-for-sale/listings/location-austin-tx"]


    def parse(self, response):
        for car in response.xpath("//ul[@class='row mb-3']/li"):
            title = car.xpath(".//div[contains(@class, 'vehicle-card-top')]/div/div/span[contains(@class, 'truncate')]/text()").get()
            yield {
                "title": title
            }


# class TruecarTxSpider(scrapy.Spider):
#     name = "truecar_tx"
#     allowed_domains = ["www.military.truecar.com"]
#     start_urls = ["https://military.truecar.com/used-cars-for-sale/listings/location-austin-tx"]

#     def parse(self, response):
#         for car in response.xpath("//ul[@class='row mb-3']/li/div/div/div[@class='card-content order-3 vehicle-card-body']"):
#             yield {
#                 "title": car.xpath(".//span[contains(@class, 'truncate')]/text()").get(),
#                 "year": car.xpath(".//span[contains(@class, 'vehicle-card-year')]/text()").get()
#             }

# "//ul[@class='row mb-3']/li/div/div/div[@class='card-content order-3 vehicle-card-body']"