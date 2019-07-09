# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoSpiderItem(scrapy.Item):
    title = scrapy.Field()
    summary = scrapy.Field()
    url = scrapy.Field()
    tags = scrapy.Field()
    catalog = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    date = scrapy.Field()
    author = scrapy.Field()

    def to_dict(self):
        return {
            'title' : self.get('title'),
            'summary' : self.get('summary'),
            'url' : self.get('url'),
            'tags' : self.get('tags'),
            'catalog' : self.get('catalog'),
            'content' : self.get('content'),
            'source' : self.get('source'),
            'date' : self.get('date'),
            'author' : self.get('author')
        }


class hotInfo(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    hot_degree = scrapy.Field()

class search_content_info(scrapy.Item):
    content_title = scrapy.Field()
    content_link = scrapy.Field()
    agree_num = scrapy.Field()
    comment_num = scrapy.Field()

class search_people_info(scrapy.Item):
    user_name = scrapy.Field()
    abode = scrapy.Field()
    industry = scrapy.Field()
    workexp = scrapy.Field()
    education = scrapy.Field()
    introduction = scrapy.Field()
    answer_num = scrapy.Field()
    ask_num = scrapy.Field()
    post_num = scrapy.Field()
    column_num = scrapy.Field()
    following_num = scrapy.Field()
    follower_num = scrapy.Field()

class post_info(scrapy.Item):
    user_id = scrapy.Field()
    post_title = scrapy.Field()
    post_link = scrapy.Field()
    agree_num = scrapy.Field()
    comment_num = scrapy.Field()

class question_answer_info(scrapy.Item):
    question_id = scrapy.Field()
    answer_people_name = scrapy.Field()
    answer_people_intro = scrapy.Field()
    agree_num = scrapy.Field()
    comment_num = scrapy.Field()

class search_people_by_content_info(scrapy.Item):
    key = scrapy.Field()
    user_name = scrapy.Field()
    link = scrapy.Field()
    num_answer = scrapy.Field()
    num_article = scrapy.Field()
    num_focus = scrapy.Field()
