# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse, Response
from .driver import zhihu_driver
from lxml import etree
import requests
import json

class ZhihucrawlerSpiderMiddleware(object):
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


class ZhihucrawlerDownloaderMiddleware(object):
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

        if key == 'page':
            content = zhihu_driver.GetValidDriverForPage(url=url, key=key).page_source
            response = HtmlResponse(url=url, request=request, body=content, encoding='utf-8')
        else:
            if key == 'content_zhuanlan':
                token = request.meta['token']
                fields = ','.join(['text', ])
                params = {
                    'token': token,
                    'url': url,
                    'fields': fields
                }

                result = requests.get('http://api.url2io.com/article', params=params)
                content = result.json()
                driver = zhihu_driver.GetValidDriverForPage(url, key)
                author = driver.find_element_by_xpath(
                    '//div[@class="AuthorInfo-content"]//a[@class="UserLink-link"]'
                ).text
                tags_tags = driver.find_elements_by_xpath(
                    '//div[@class="Tag Topic"]//div[@class="Popover"]/div'
                )
                tags = []
                for tag in tags_tags: tags.append(tag.text)
                content['tags'] = tags
            else:
                driver = zhihu_driver.GetValidDriverForPage(url, key)
                p_tags = driver.find_elements_by_xpath('//p')
                text = ''
                for p in p_tags:
                    text += p.text
                content = {}
                content['text'] = text
                title_tag = driver.find_element_by_xpath('//div[@class="QuestionHeader"]//h1[@class="QuestionHeader-title"]')
                content['title'] = title_tag.text

                tags_tags = driver.find_elements_by_xpath('//div[@class="Tag QuestionTopic"]//div[@class="Popover"]/div')
                tags = []
                for tag in tags_tags: tags.append(tag.text)
                content['tags'] = tags
                content['date'] = ''
                author = ''
            content['author'] = author
            response = Response(url=request.url, body=json.dumps(content, ensure_ascii=False).encode(encoding='utf-8'),
                                request=request)
        return response

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
