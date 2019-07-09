# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import *
# import pymysql

# class ZhihucrawlerPipeline(object):
#     SQL_Queries_List = {
#         'people_id_info': 'insert into people_information (user_name, live_place, profession, work_experience, education, introduction, answer_num, ask_num, post_num, column_num, following_num, follower_num) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s") ',
#         'id_posts': 'insert into user_posts (people_id, post_title, post_link, agree_num, comment_num) values ("%s", "%s", "%s", "%s", "%s")',
#         'question_answers': 'insert into question_answers (question_id, answer_people_name, answer_people_intro, agree_num, comment_num) values ("%s", "%s", "%s", "%s", "%s")',
#         'search_contents': 'insert into search_contents (content_title, content_link, agree_num, comment_num) values ("%s", "%s", "%s", "%s")',
#         'search_people': 'insert into search_people (search_key, user_name, link, num_answer, num_article, num_focus) values ("%s", "%s", "%s", "%s", "%s", "%s")',
#         'hot': 'insert into hot (title, link, hot_degree) values ("%s", "%s", "%s")'
#     }
#     mysql_database = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='zhihu',
#                                      charset='utf8') #here to change the user and passwd, use mysql database

#     def process_item(self, item, spider):
#         if(isinstance(item, hotInfo)):
#             self.save_hot_info(item)
#         elif(isinstance(item, search_content_info)):
#             self.save_search_content_info(item)
#         elif(isinstance(item, search_people_info)):
#             self.save_search_people_info(item)
#         elif(isinstance(item, post_info)):
#             self.save_post(item)
#         elif(isinstance(item, question_answer_info)):
#             self.save_question_answer(item)
#         elif(isinstance(item, search_people_by_content_info)):
#             self.save_search_people_by_content_info(item)
#         return item

#     def insert_by_sql(self, clause):
#         try:
#             with self.mysql_database.cursor() as cursor:
#                 cursor.execute(clause)
#             self.mysql_database.commit()
#         except Exception as e:
#             self.mysql_database.rollback()
#             return

#     def save_hot_info(self, item):
#         sql_clause = self.SQL_Queries_List['hot'] % (item.get("title"), item.get("link"), item.get("hot_degree"))
#         self.insert_by_sql(sql_clause)

#     def save_search_content_info(self, item):
#         sql_clause = self.SQL_Queries_List['search_contents'] % (item.get('content_title'), item.get('content_link'), item.get('agree_num'), item.get('comment_num'))
#         self.insert_by_sql(sql_clause)

#     def save_search_people_info(self, item):
#         sql_clause = self.SQL_Queries_List['people_id_info'] % (item.get('user_name'), item.get('abode'), item.get('industry'), item.get('workexp'),
#         item.get('education'), item.get('introduction'), item.get('answer_num'), item.get('ask_num'), item.get('post_num'), item.get('column_num'), item.get('following_num'), item.get('follower_num'))
#         self.insert_by_sql(sql_clause)

#     def save_post(self, item):
#         sql_clause = self.SQL_Queries_List['id_posts'] % (item.get('user_id'), item.get('post_title'), item.get('post_link'), item.get('agree_num'), item.get('comment_num'))
#         self.insert_by_sql(sql_clause)

#     def save_question_answer(self, item):
#         sql_clause = self.SQL_Queries_List['question_answers'] % (item.get('question_id'), item.get('answer_people_name'), item.get('answer_people_intro'), item.get('agree_num'), item.get('comment_num'))
#         self.insert_by_sql(sql_clause)

#     def save_search_people_by_content_info(self, item):
#         sql_clause = self.SQL_Queries_List['search_people'] % (item.get('key'), item.get('user_name'), item.get('link'), item.get('num_answer'), item.get('num_article'), item.get('num_focus'))
#         self.insert_by_sql(sql_clause)

from scrapy.exporters import JsonItemExporter,JsonLinesItemExporter
class JsonWriterPipeline(object):

    def __init__(self):
        self.files = {}
    
    def open_spider(self, spider): #
        file = open('%s_ip.json' % spider.name, 'w+b') # 生成文件描述符
        self.files[spider] = file # 保存描述符的引用
        self.exporter = JsonLinesItemExporter(file) # 实例化一个Exporter类
        self.exporter.start_exporting() # 开始输出
 
    def close_spider(self,spider):
        self.exporter.finish_exporting() # 结束输出
        #print('*'*50)
        file = self.files.pop(spider)
        #print(file.name)
        file.close()
        
    def process_item(self, item, spider):
        self.exporter.export_item(item) # 正式输出
        return item

import pymongo
import json

class DemoSpiderPipeline(object):
    def __init__(self):
        with open('config.json', 'r') as cursor:
            self.CONFIG = json.load(cursor)

        mongo_url = 'mongodb://{}:{},{}:{},{}:{}'.format(
            self.CONFIG['MONGO_HOST'], self.CONFIG['MONGO_PORT_1'],
            self.CONFIG['MONGO_HOST'], self.CONFIG['MONGO_PORT_2'],
            self.CONFIG['MONGO_HOST'], self.CONFIG['MONGO_PORT_3'],
        )
        self.mongo_client = pymongo.MongoClient(mongo_url)
        self.mongo_db = self.mongo_client[self.CONFIG['MONGO_DATABASE']]
        self.mongo_collection = self.mongo_db[self.CONFIG['MONGO_COLLECTION']]

    def process_item(self, item, spider):
        document = item
        document = document.to_dict()
        self.mongo_collection.insert_one(document=document)
        return item

    def close_spider(self, spider):
        self.mongo_client.close()