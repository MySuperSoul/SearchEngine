# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json

class ZhihucrawlerPipeline(object):
    def __init__(self):
        with open('config.json', 'r') as cursor:
            self.CONFIG = json.load(cursor)

        self.mongo_client = pymongo.MongoClient(self.CONFIG['MONGO_HOST'], self.CONFIG['MONGO_PORT'])
        self.mongo_db = self.mongo_client[self.CONFIG['MONGO_DATABASE']]
        self.mongo_collection = self.mongo_db[self.CONFIG['MONGO_COLLECTION']]

    def process_item(self, item, spider):
        document = item
        document = document.to_dict()
        self.mongo_collection.insert_one(document=document)
