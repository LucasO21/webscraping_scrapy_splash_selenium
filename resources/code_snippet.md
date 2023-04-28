# Scrapy Syntax To Start Project & Spider

* Create a new scrapy project: ```scrapy startproject <project_name>```
* Create a spider: ```scrapy genspider <spider_name> <url>```. Make sure to delete trailing ```/``` and ```https://```

* Save scraped dataset: ```scrapy crawl countries -o <dataset_name>.json```

# Check For & Close Any Headless Drivers

* Check for open headless drivers: ``` ps aux | grep "chromedriver" ```

* Quit all open headless drivers: ``` "pkill -f "chromedriver" ```
