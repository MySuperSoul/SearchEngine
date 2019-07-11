import scrapy
import json
import os
from scrapy.http import Request
from bs4 import BeautifulSoup
from ..items import DemoSpiderItem
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from ..driver import DemoDriver

class DemoSpider(scrapy.Spider):
    name = 'demo-spider'
    start_url = 'https://www.jianshu.com/search?q=%s&page=%d'
    host = 'https://www.jianshu.com'

    def __init__(self):
        config_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'config.json')
        with open(config_path, 'r') as cursor:
            self.CONFIG = json.load(cursor)
        self.keywords_map = {keyword: False for keyword in self.CONFIG['keywords']}

        dispatcher.connect(self.SpiderStopped, signals.engine_stopped)

    def SpiderStopped(self):
        for driver in DemoDriver.driver_pools:
            driver.close()

    def parse(self, response):
        pass

    def start_requests(self):
        for keyword in self.CONFIG['keywords']:
            url = self.start_url % (keyword, 1)
            yield Request(url, callback=self.parse_page, meta={
                'key' : 'page',
                'keyword' : keyword
            })

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        content_tags = soup.find_all('div', class_='content')
        for tag in content_tags:
           content_url = self.host + tag.contents[2].get('href')
           yield Request(content_url, callback=self.parse_content, meta={
               'key' : 'content',
               'keyword' : response.meta['keyword'],
               'token' : self.CONFIG['token']
           })

        # calculate all pages
        if self.keywords_map[response.meta['keyword']] == False:
            result_tag = soup.find('div', class_='result')
            result = int(result_tag.text.split()[0])
            total_pages = result // 10
            for page in range(2, min(100, total_pages)):
                yield Request(self.start_url % (response.meta['keyword'], page), callback=self.parse_page, meta={
                    'key' : 'page',
                    'keyword' : response.meta['keyword']
                })
            self.keywords_map[response.meta['keyword']] = True

    def parse_content(self, response):
        content = bytes.decode(response.body, encoding='utf-8')
        info_dic = json.loads(content)
        info_dic['summary'] = ''
        info_dic['url'] = response.url
        info_dic['catalog'] = self.CONFIG['catalog']
        keyword = response.meta['keyword']
        info_dic['tags'] = [keyword]
        info_dic['source'] = self.CONFIG['source']

        document = DemoSpiderItem()
        document['title'] = info_dic['title'],
        document['summary'] = info_dic['summary'],
        document['url'] = info_dic['url'],
        document['tags'] = info_dic['tags'],
        document['catalog'] = info_dic['catalog'],
        document['content'] = info_dic['text'],
        document['source'] = info_dic['source'],
        document['date'] = info_dic['date'],
        document['author'] = info_dic['author']

        yield document