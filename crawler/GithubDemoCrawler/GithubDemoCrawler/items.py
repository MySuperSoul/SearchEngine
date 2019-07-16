# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubdemocrawlerItem(scrapy.Item):
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
            'title': self.get('title'),
            'summary': self.get('summary'),
            'url': self.get('url'),
            'tags': self.get('tags'),
            'catalog': self.get('catalog'),
            'content': self.get('content'),
            'source': self.get('source')[0],
            'date': self.get('date'),
            'author': self.get('author')
        }
