import scrapy
import json
import os
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
    start_tag_url = 'https://stackoverflow.com/questions/tagged/%s?page=%d'
    host = 'https://stackoverflow.com'

    def __init__(self):
        super(STOSpider, self).__init__()

        config_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'config.json')
        with open(config_path, 'r') as cursor:
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
                'keyword' : keyword,
                'tag' : 0
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
            # Judge whether tagged problem
            tagged_flag = False
            result_tag = selector.xpath('//h1[contains(@class, "grid--cell")]')[0]
            result = str(result_tag.text)
            if result.find('tagged') != -1:
                tagged_flag = True

            # calculate all pages
            page_number_tags = selector.xpath('//span[@class="page-numbers"]')
            pages = int(page_number_tags[-1].text)
            for page in range(2, min(pages + 1, 101)):
                if tagged_flag == False:
                    yield Request(url=self.start_url % (page, response.meta['keyword']),
                                  callback=self.parse_page,
                                  meta={
                                      'key' : 'page',
                                      'tag' : 0,
                                      'keyword' : response.meta['keyword']
                                  })
                else:
                    yield Request(url=self.start_tag_url % (response.meta['keyword'], page),
                                  callback=self.parse_page,
                                  meta={
                                      'key' : 'page',
                                      'tag' : 1,
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


