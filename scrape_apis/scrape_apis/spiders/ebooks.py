import scrapy
import json
from scrapy.exceptions import CloseSpider


class EbooksSpider(scrapy.Spider):
    name = "ebooks"
    
    INCREMENT_BY = 12
    offset = 0
    
    allowed_domains = ["openlibrary.org"]
    start_urls = ["https://openlibrary.org/subjects/picture_books.json?limit=12"]

    def parse(self, response):
        
        if response.status == 500:
            raise CloseSpider("Reached last page...")
        
        resp = json.loads(response.body)
        ebooks = resp.get("works")

        data = []
        for ebook in ebooks:
            data.append({
                "title": ebook.get("title"),
                "subject": ebook.get("subject")
            })
            
        self.offset += self.INCREMENT_BY
        yield scrapy.Request(
            url = f"https://openlibrary.org/subjects/picture_books.json?limit=12&offset={self.offset}",
            callback = self.parse
        )

        with open("data/ebooks.json", "w") as f:
            json.dump(data, f)


        for ebook in ebooks:
            data.append({
                "title": ebook.get("title"),
                "subject": ebook.get("subject")
        })