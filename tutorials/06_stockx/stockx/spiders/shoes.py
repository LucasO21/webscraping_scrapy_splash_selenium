import scrapy


class ShoesSpider(scrapy.Spider):
    name = "shoes"
    allowed_domains = ["www.stockx.com"]
    #start_urls = ["https://www.stockx.com/sneakers"]
    
     # spoof request headers
    def start_requests(self):
        yield scrapy.Request(
            url      = "https://www.stockx.com/sneakers", 
            callback = self.parse, 
            headers  = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"}
        )    
    
    # get product urls from opening page
    def parse(self, response):
        for shoe in response.xpath("//div[@class='css-111hzm2-GridProductTileContainer']/div[@class='css-pnc6ci']"):
            
            url = response.urljoin(shoe.xpath("./a/@href").get(default = "NA"))
            name = shoe.xpath(".//p[@class='chakra-text css-3lpefb']/text()").get(default = "NA").strip()
            price = shoe.xpath(".//p[@class='chakra-text css-nsvdd9']/text()").get(default = "NA").strip()
            image_url = shoe.xpath(".//div[@class='css-tkc8ar']/img/@srcset[1]").get(default = "NA")


            # follow each url to scrape data
            # yield scrapy.Request(
            #     "url": url, 
            #     "shoe_name": shoe_name,
            #     callback = self.parse_shoe_page,
            #     headers  = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"}
            # )
            
            yield {
                "url": url,
                "name": name,
                "price": price,
                "image_url": image_url
                
            }
            
    
    # # scrape shoe information
    # def parse_shoe_page(self, response):
    #     url = response.url
    #     count_sold_last_30_days = response.xpath("//h2[@class='chakra-heading css-15n3kqp']/text()").get(default = "NA").strip()
            
            
    #     # final yield
    #     yield {
    #          "url": url
    #         , "count_sold_last_30_days": count_sold_last_30_days
    #     }


    



