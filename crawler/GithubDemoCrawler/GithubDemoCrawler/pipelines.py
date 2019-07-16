# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json
import os

class GithubdemocrawlerPipeline(object):
    def open_spider(self, spider):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
        with open(config_path, 'r') as cursor:
            self.CONFIG = json.load(cursor)

        mongo_url = 'mongodb://{}:{},{}:{},{}:{}'.format(
            self.CONFIG['MONGO_HOST'], self.CONFIG['MONGO_PORT_1'],
            self.CONFIG['MONGO_HOST'], self.CONFIG['MONGO_PORT_2'],
            self.CONFIG['MONGO_HOST'], self.CONFIG['MONGO_PORT_3'],
        )

        # mongo_url = 'mongodb://localhost:27017'

        self.mongo_client = pymongo.MongoClient(mongo_url)
        self.mongo_db = self.mongo_client[self.CONFIG['MONGO_DATABASE']]
        self.mongo_collection = self.mongo_db[self.CONFIG['MONGO_COLLECTION']]

    def process_item(self, item, spider):
        document = item
        document = document.to_dict()
        print('Finish {}'.format(document['url']))
        self.mongo_collection.insert_one(document=document)

    def close_spider(self, spider):
        self.mongo_client.close()
