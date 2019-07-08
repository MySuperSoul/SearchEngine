import scrapy
import json
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http import Request
from ..driver import zhihu_driver
from bs4 import BeautifulSoup
from lxml import etree
from ..utils import Catalog
from ..items import ZhihucrawlerItem

class ZhiHuSpider(scrapy.Spider):
    name = 'zhihu-spider'
    start_url = 'https://www.zhihu.com/search?type=content&q=%s'

    def __init__(self):
        with open('config.json', 'r') as cursor:
            self.CONFIG = json.load(cursor)

        dispatcher.connect(self.SpiderStopped, signals.engine_stopped)

    def SpiderStopped(self):
        for driver in zhihu_driver.driver_pools:
            driver.quit()
            driver.close()

    def start_requests(self):
        for keyword in self.CONFIG['keywords']:
            url = self.start_url % keyword
            yield Request(url, callback=self.parse_page_urls, meta={
                'keyword' : keyword,
                'key' : 'page'
            })

    def parse_page_urls(self, response):
        keyword = response.meta['keyword']
        selector = etree.HTML(response.text)
        links = selector.xpath('//h2[@class="ContentItem-title"]//a[not(@class)]/@href')

        for link in links:
            url = str(link)
            if url.find('zhuanlan') != -1: # zhuanlan article
                url = 'https:' + url
                yield Request(url=url, callback=self.parse_content, meta={
                    'keyword' : response.meta['keyword'],
                    'key' : 'content_zhuanlan',
                    'token' : self.CONFIG['token']
                })
            else:
                url = 'https://www.zhihu.com' + url
                yield Request(url=url, callback=self.parse_content, meta={
                    'keyword': response.meta['keyword'],
                    'key': 'content_qa',
                    'token': self.CONFIG['token']
                })

    def parse_content(self, response):
        content = bytes.decode(response.body, encoding='utf-8')
        info_dic = json.loads(content)
        info_dic['summary'] = ''
        info_dic['url'] = response.url
        if response.meta['key'] == 'content_zhuanlan':
            info_dic['catalog'] = Catalog.CATALOG_BLOG
        else:
            info_dic['catalog'] = Catalog.CATALOG_QA

        keyword = response.meta['keyword']
        info_dic['tags'] = [keyword]
        info_dic['source'] = self.CONFIG['source']

        document = ZhihucrawlerItem()

        document['title'] = info_dic['title'],
        document['summary'] = info_dic['summary'],
        document['url'] = info_dic['url'],
        document['tags'] = info_dic['tags'],
        document['catalog'] = info_dic['catalog'],
        document['content'] = info_dic['text'].strip('\n'),
        document['source'] = info_dic['source'],
        document['date'] = info_dic['date'],
        document['author'] = info_dic['author']

        yield document