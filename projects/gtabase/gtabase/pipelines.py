# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import os
import re

# Data Cleaning Pipeline
class GtabaseCleanPipeline:
    def process_item(self, item, spider):
        item = ItemAdapter(item)
        
        vehicle_name = item.get("vehicle_name")
        manufacturer = item.get("manufacturer")
        acquisition = item.get("acquisition")
        storage = item.get("storage")
        modification = item.get("modification")
        sell = item.get("sell")
        sell_price = item.get("sell_price")
        sell_price_fully_upgraded = item.get("sell_price_fully_upgraded")
        race_availability = item.get("race_availability")
        top_speed = item.get("top_speed")
        based_on = item.get("based_on")  
        
        try:
            item["vehicle_name"] = re.sub(': GTA V Vehicle Info', '', vehicle_name)
            item["manufacturer"] = manufacturer
            item["acquisition"] = acquisition
            item["storage"] = storage
            item["modification"] = modification
            item["sell"] = sell
            item["sell_price"] = int(re.sub(r'[^\d.]', '', sell_price))
            item["sell_price_fully_upgraded"] = int(re.sub(r'[^\d.]', '', sell_price_fully_upgraded))
            item["race_availability"] = race_availability
            item["top_speed"] = float(top_speed.split(" ")[0])
            item["based_on"] = based_on        
        except:
            item["vehicle_name"] = vehicle_name
            item["manufacturer"] = manufacturer
            item["acquisition"] = acquisition
            item["storage"] = storage
            item["modification"] = modification
            item["sell"] = sell
            item["sell_price"] = sell_price
            item["sell_price_fully_upgraded"] = sell_price_fully_upgraded
            item["race_availability"] = race_availability
            item["top_speed"] = top_speed
            item["based_on"] = based_on
                        
            
        return item


        
# SQL Lite DB Pipeline
class GtabaseSqllitePipeline:
    
    def open_spider(self, spider):
        # if os.path.exists("database/vehicles.db"):
        #     os.remove("database/vehicles.db")        
        #     os.makedirs("database")
            
        db_file = os.path.join("database", "vehicles.db")
        self.connection = sqlite3.connect(db_file)
        self.c = self.connection.cursor()
        try:
            self.c.execute(
                '''
                CREATE TABLE vehicles(
                    
                    vehicle_name TEXT,
                    manufacturer TEXT,
                    acquisition TEXT,
                    storage TEXT,
                    modification TEXT,
                    sell TEXT,
                    sell_price NUMERIC,
                    sell_price_fully_upgraded TEXT,
                    race_availability TEXT,
                    top_speed NUMERIC,
                    based_on TEXT 
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
            INSERT INTO vehicles (
                vehicle_name,
                manufacturer,
                acquisition,
                storage,
                modification,
                sell,
                sell_price,
                sell_price_fully_upgraded,
                race_availability,
                top_speed,
                based_on 
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?)
            ''',
            (
                item.get("vehicle_name"),
                item.get("manufacturer"),
                item.get("acquisition"),
                item.get("storage"),
                item.get("modification"),
                item.get("sell"),
                item.get("sell_price"),
                item.get("sell_price_fully_upgraded"),
                item.get("race_availability"),
                item.get("top_speed"),
                item.get("based_on")
            )
        )        
        
        self.connection.commit()
        
        return item