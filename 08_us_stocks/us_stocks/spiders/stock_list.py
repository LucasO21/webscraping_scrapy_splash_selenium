import scrapy

class StockListSpider(scrapy.Spider):
    name = "stock_list"
    allowed_domains = "www.tradingview.com"
    
    def start_requests(self):
        yield scrapy.Request(
            url      = "https://www.tradingview.com/markets/stocks-usa/sectorandindustry-industry/", 
            callback = self.parse, 
            headers  = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"}
        )
    
    
    def parse(self, response):
        for stock in response.xpath("//tr[@class='row-EdyDtqqh listRow']/td"):
            
            url     = response.urljoin(stock.xpath(".//a[@class='link-j5JxgHa0 apply-common-tooltip industryTickerCell-vVPXFiXD']/@href").get())         
            
            yield scrapy.Request(
                url      = url,
                callback = self.parse_stock_list,
                headers  = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"}
            )
    
    
    def parse_stock_list(self, response):
        industry = response.xpath("//h1[@class='tv-category-header__title-text']/text()").get().strip()
            
        yield {
            "industry": industry
        }