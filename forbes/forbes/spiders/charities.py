import scrapy


class CharitiesSpider(scrapy.Spider):
    name = "charities"
    allowed_domains = ["www.forbes.com"]
    #start_urls = ["https://www.forbes.com/lists/top-charities"]
    
    # spoof request
    def start_requests(self):
        yield scrapy.Request(url = "https://www.forbes.com/lists/top-charities", callback = self.parse, headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"
        })
    
    # scrape first page
    def parse(self, response):        
        for charity in response.xpath("//div[@class='table-row-group']/a[contains(@class, 'table-row active')]"):
            
            rank              = charity.xpath(".//div[@class='rank first table-cell    rank']/text()").get().strip()
            name              = charity.xpath(".//div[@class='organizationName second table-cell    name']/text()").get().strip()
            category          = charity.xpath(".//div[@class='industry  table-cell    category']/text()").get().strip()      
            url               = charity.xpath("./@href").get()
            
            # follow each URL and call the `parse_charity_page` method to extract additional data
            yield scrapy.Request(
                url, 
                callback = self.parse_charity_page, 
                headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"},
                meta = {
                    "rank":         rank,
                    "name":         name,
                    "category":     category
                }
            )
            
    # scrape additional data points        
    def parse_charity_page(self, response):
        rank                = response.meta["rank"]
        name                = response.meta["name"]
        category            = response.meta["category"]
        headquarters        = response.xpath("//div[@class='listuser-block__item'][2]/span[text()='Headquarters']/following-sibling::span/span/text()").get().strip()      
        ceo                 = response.xpath("//div[@class='listuser-block__item'][4]/span[text()='Top Person']/following-sibling::span/span/text()").get().strip()      
        total_revenue       = response.xpath("//div[@class='listuser-content__block person-stats'][2]/div[3]/span[2]/span/text()").get().strip()
        private_donations   = response.xpath("//div[@class='listuser-content__block person-stats'][2]/div[3]/span/div/div[2]/div/span[text()='Private Donations']/following-sibling::span/text()").get().strip()
        other_income        = response.xpath("//div[@class='listuser-content__block person-stats'][2]/div[3]/span/div/div[2]/div/span[text()='Other Income']/following-sibling::span/text()").get().strip()
        total_expenses      = response.xpath("//div[@class='listuser-content__block person-stats'][2]/div[4]/span[2]/span/text()").get().strip()
        charitable_services = response.xpath("//div[@class='listuser-content__block person-stats'][2]/div[4]/span/div/div[2]/div/span[text()='Charitable Services']/following-sibling::span/text()").get().strip()
        mgt_and_general     = response.xpath("//div[@class='listuser-content__block person-stats'][2]/div[4]/span/div/div[2]/div/span[text()='Management & General']/following-sibling::span/text()").get().strip()
        fundraising         = response.xpath("//div[@class='listuser-content__block person-stats'][2]/div[4]/span/div/div[2]/div/span[text()='Fundraising']/following-sibling::span/text()").get().strip()
        surplus_loss        = response.xpath("//div[@class='listuser-content__block person-stats'][2]/div[5]/span[2]/span/text()").get().strip()
        net_assets          = response.xpath("//div[@class='listuser-content__block person-stats'][2]/div[6]/span[2]/span/text()").get().strip()
        charitable_commitment = response.xpath("//div[@class='listuser-content__block person-stats'][2]/div[7]/span[2]/span/text()").get().strip()
        fundraising_efficiency = response.xpath("//div[@class='listuser-content__block person-stats'][2]/div[8]/span[2]/span/text()").get().strip()
        donor_dependency       = response.xpath("//div[@class='listuser-content__block person-stats'][2]/div[9]/span[2]/span/text()").get().strip()
        highest_compensation   = response.xpath("//div[@class='listuser-content__block person-stats'][2]/div[10]/span[2]/span/text()").get().strip()    
         
         
        # final yield
        yield {       
              "rank":                   rank
            , "name":                   name
            , "category":               category
            , "headquarters":           headquarters
            , "ceo":                    ceo
            , "total_revenue":          total_revenue
            , "private_donations":      private_donations
            , "other_income":           other_income
            , "total_expenses":         total_expenses
            , "charitable_services":    charitable_services
            , "management_&_general":   mgt_and_general
            , "fundraising":            fundraising
            , "surplus/loss":           surplus_loss
            , "net_assets":             net_assets
            , "charitable_commitment":  charitable_commitment
            , "fundraising_efficiency": fundraising_efficiency
            , "donor_dependency":       donor_dependency
            , "highest_compensation":   highest_compensation
            , "url":                    response.url            
        }

