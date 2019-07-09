import scrapy
import json
from ..driver import sto_driver
from scrapy import signals
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from lxml import etree
from CrawlerUtils.Catalog import DocCatalog

class STOSpider(scrapy.Spider):
    name = 'sto-spider'
    start_url = 'https://stackoverflow.com/search?page=%d&q=%s'
    host = 'https://stackoverflow.com'

    def __init__(self):
        super(STOSpider, self).__init__()

        with open('config.json', 'r') as cursor:
            self.CONFIG = json.load(cursor)

        self.keywords_map = {keyword: False for keyword in self.CONFIG['keywords']}
        dispatcher.connect(self.SpiderStopped, signals.engine_stopped)

    def SpiderStopped(self):
        for driver in sto_driver.driver_pools:
            driver.close()

    def start_requests(self):
        for keyword in self.CONFIG['keywords']:
            yield Request(url=self.start_url % (1, keyword), callback=self.parse_page, meta={
                'key' : 'page',
                'keyword' : keyword
            })

    def parse_page(self, response):
        content = response.text
        selector = etree.HTML(content)
        link_tags = selector.xpath('//div[@class="summary"]//h3/a')

        for link in link_tags:
            link_url = self.host + link.get('href')
            yield Request(url=link_url, callback=self.parse_content, meta={
                'key' : 'content',
                'keyword' : response.meta['keyword'],
                'token' : self.CONFIG['token']
            })

    def parse_content(self, response):
        pass

