import scrapy
import json
import os
from scrapy import signals
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from CrawlerUtils.Catalog import DocCatalog
from ..driver import github_driver
from ..items import GithubdemocrawlerItem
from lxml import etree

class GithubDemoSpider(scrapy.Spider):
    name = 'github-spider'
    start_url = 'https://github.com/search?p=%d&q=%s&type=Repositories'
    host = 'https://github.com'
    keywords_map = {}

    def __init__(self):
        super(GithubDemoSpider, self).__init__()

        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')
        with open(config_path, 'r') as cursor:
            self.CONFIG = json.load(cursor)

        for keyword in self.CONFIG['keywords']:
            self.keywords_map[keyword] = False

        dispatcher.connect(self.SpiderStopped, signals.engine_stopped)

    def SpiderStopped(self):
        for driver in github_driver.driver_pools:
            driver.close()

    def start_requests(self):
        for keyword in self.CONFIG['keywords']:
            url = self.start_url % (1, keyword)
            yield Request(url=url, callback=self.parse_page, meta={
                'key' : 'page',
                'keyword' : keyword
            })

    def parse_page(self, response):
        content = response.text
        selector = etree.HTML(content)
        repo_list_tags = selector.xpath('//li[contains(@class, "repo-list-item")]/div[1]')

        for repo in repo_list_tags:
            a_tag = repo.find('./h3/a[1]')
            link = self.host + a_tag.get('href')
            yield Request(url=link, callback=self.parse_content, meta={
                'key' : 'content',
                'keyword' : response.meta['keyword'],
            })

        # crawl pages
        if self.keywords_map[response.meta['keyword']] == False:
            # last_page = selector.xpath('//em[@class="current"]')
            # total_page = int(last_page[0].get('data-total-pages'))

            for page in range(2, 20):
                yield Request(url=self.start_url % (page, response.meta['keyword']), callback=self.parse_page, meta={
                    'key' : 'page',
                    'keyword' : response.meta['keyword']
                })

            self.keywords_map[response.meta['keyword']] = True

    def parse_content(self, response):
        content = response.text
        selector = etree.HTML(content)
        try:
            summary_tag = selector.xpath('//span[@class="text-gray-dark mr-2"]')[0]
            summary = ' '.join(summary_tag.text.strip('\n').split())

            date_tag = selector.xpath('//relative-time')[0]
            date = date_tag.text

            url = response.url
            url_text = url.split('/')
            author = url_text[-2]
            title = url_text[-1]

            document = GithubdemocrawlerItem()
            document['title'] = title
            document['summary'] = summary
            document['url'] = url
            document['tags'] = [response.meta['keyword']]
            document['catalog'] = DocCatalog.CATALOG_DEMO
            document['content'] = summary
            document['source'] = self.CONFIG['source'],
            document['author'] = author
            document['date'] = date

            yield document
        except Exception as e:
            pass
