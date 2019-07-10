import scrapy
import json
from ..driver import sto_driver
from ..items import StocrawlerItem
from scrapy import signals
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from lxml import etree
from CrawlerUtils.Catalog import DocCatalog
from CrawlerUtils.Utils import Utils

class STOSpider(scrapy.Spider):
    name = 'sto-spider'
    start_url = 'https://stackoverflow.com/search?page=%d&q=%s&tab=Relevance'
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

        # get total pages
        if self.keywords_map[response.meta['keyword']] == False:
            page_number_tags = selector.xpath('//span[@class="page-numbers"]')
            pages = int(page_number_tags[-1].text)
            for page in range(2, pages + 1):
                yield Request(url=self.start_url % (page, response.meta['keyword']),
                              callback=self.parse_page,
                              meta={
                                  'key' : 'page',
                                  'keyword' : response.meta['keyword']
                              })
            self.keywords_map[response.meta['keyword']] = True

    def parse_content(self, response):
        content = Utils.GetInfoDicFromBytes(content=response.body)

        content['catalog'] = DocCatalog.CATALOG_QA
        content['source'] = self.CONFIG['source']
        content['summary'] = ''

        document = StocrawlerItem()
        document = Utils.FeedDocument(document=document, info_dic=content)

        yield document


