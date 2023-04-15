# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import os
import sqlite3

# Mongo DB Pipeline
# class MongodbPipeline:
    
#     collection_name = "us_top_charities"    
  
#     # username = os.environ.get("MONGO_DB_WEBSCRAPING_USER")
#     # password = os.environ.get("MONGO_DB_WEBSCRAPING_PASS")
#     # mongo_connect = f"mongodb+srv://{username}:{password}@clusterwebscraping.uhxywhe.mongodb.net/?retryWrites=true&w=majority"
    
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient("self.mongo_connect")
#         self.db = self.client["FORBES"]
        
#     def close_spider(self, spider):
#         self.client.close()
    
#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert(item)
#         return item


# SQLLite3 Pipeline
class SQLitePipeline:  
    
    def open_spider(self, spider):
        db_file = os.path.join("database", "charities.db")
        self.connection = sqlite3.connect(db_file)
        self.c = self.connection.cursor()
        try:
            self.c.execute(
                '''
                CREATE TABLE us_top_charities(
                    rank TEXT,
                    charity_name TEXT,
                    category TEXT,
                    headquarters TEXT,
                    ceo TEXT,
                    total_revenue TEXT,
                    private_donations TEXT,
                    other_income TEXT,
                    total_expenses TEXT,
                    charitable_services TEXT,
                    management_general TEXT,
                    fundraising TEXT,
                    surplus_loss TEXT,
                    net_assets TEXT,
                    charitable_commitment TEXT,
                    fundraising_efficiency TEXT,
                    donor_dependency TEXT,
                    highest_compensation TEXT,
                    charity_url TEXT        
                )           
                
                '''
            )
        
            self.connection.commit()
        except sqlite3.OperationalError:
            pass
        
    def close_spider(self, spider):
        self.connection.close()
    
    def process_item(self, item, spider):
        self.c.execute(
            '''
            INSERT INTO us_top_charities (
                rank,
                charity_name,
                category,
                headquarters,
                ceo,
                total_revenue,
                private_donations,
                other_income,
                total_expenses,
                charitable_services,
                management_general,
                fundraising,
                surplus_loss,
                net_assets,
                charitable_commitment,
                fundraising_efficiency,
                donor_dependency,
                highest_compensation,
                charity_url  
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''',
            (
                item.get('rank'),
                item.get('charity_name'),
                item.get('category'),
                item.get('headquarters'),
                item.get('ceo'),
                item.get('total_revenue'),
                item.get('private_donations'),
                item.get('other_income'),
                item.get('total_expenses'),
                item.get('charitable_services'),
                item.get('management_general'),
                item.get('fundraising'),
                item.get('surplus_loss'),
                item.get('net_assets'),
                item.get('charitable_commitment'),
                item.get('fundraising_efficiency'),
                item.get('donor_dependency'),
                item.get('highest_compensation'),
                item.get('charity_url')
            )
        )        
        
        self.connection.commit()
        
        return item
