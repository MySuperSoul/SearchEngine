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
            'title': self.get('title')[0],
            'summary': self.get('summary')[0],
            'url': self.get('url')[0],
            'tags': self.get('tags')[0],
            'catalog': self.get('catalog')[0],
            'content': self.get('content')[0],
            'source': self.get('source')[0],
            'date': self.get('date')[0],
            'author': self.get('author')
        }
