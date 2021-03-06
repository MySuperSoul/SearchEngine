# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from .driver import sto_driver
from scrapy.http import HtmlResponse, Response
from CrawlerUtils.Utils import Utils
from lxml import etree
import json

class StocrawlerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class StocrawlerDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        url = request.url
        key = request.meta['key']
        driver = sto_driver.GetValidDriverForPage(url=url, key=key)

        if key == 'page':
            return HtmlResponse(url=url, body=driver.page_source, encoding='utf-8', request=request)
        else:
            content = Utils.GetPageContent(token=request.meta['token'], url=url)

            page = sto_driver.GetValidDriverForPage(url=url, key=key).page_source
            selector = Utils.GetSelectorForText(page)

            date_tag = selector.xpath('//p[@class="label-key" and (@title)]')
            date = date_tag[0].get('title')
            content['date'] = date[:-1]

            author_tag = selector.xpath('//div[@class="user-details"]//a')
            author = author_tag[0].text
            content['author'] = author

            title_tag = selector.xpath('//a[@class="question-hyperlink"]')
            title = title_tag[0].text
            content['title'] = title

            tags = selector.xpath('//a[@class="post-tag js-gps-track"]')
            doc_tags = []
            for tag in tags: doc_tags.append(tag.text)
            content['tags'] = doc_tags

            content['text'] = content['text'].strip().strip('\n')

            return Response(url=url, request=request, body=Utils.GetResponseForJson(content=content))

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
