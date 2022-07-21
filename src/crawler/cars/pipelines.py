# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from itemadapter import ItemAdapter
# from settings import DB_LOCATION
# from items import CarsItem

import os

class CarsPipeline:

    def __init__(self):
        pass
        self.create_connection()
        self.create_table()

    def create_connection(self):
        if not os.path.isdir(r"./../output"):
            os.makedirs("./../output")
        self.conn = sqlite3.connect(r"./../output/cars.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""
            create table car(
                naziv text NOT NULL,
                cena number,
                godiste number,
                gorivo text
            ) 
        """)

    def process_item(self, item, spider):
        return item
