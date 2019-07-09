# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse,Response
from fake_useragent import UserAgent
from .drivers import *
import requests
import json
from zhihucrawler.settings import IPPOOL

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
    token="DEtqS8TIQi-9ePwdtkzZXw"

    def __init__(self, crawler):
        super(ZhihucrawlerDownloaderMiddleware, self).__init__()
        self.ua = UserAgent()
        # 可读取在settings文件中的配置，来决定开源库ua执行的方法，默认是random，也可是ie、Firefox等等
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        key = request.meta["key"] if request.meta.get("key") is not None else []
        # if(key == 'hot'):
        #     cookie = request.meta['cookie']
        #     Agent = request.meta['agent']
        #     headers = {
        #         'User-Agent': Agent,
        #         'Referer': "https://www.zhihu.com/",
        #         'Cookie': cookie  # login with cookie
        #     }
        #
        #     # use requests to send the request to website
        #     res = requests.get("https://www.zhihu.com/hot", headers=headers)
        #     html = res.text
        #     return HtmlResponse(request.url, encoding='utf-8', body=html, request=request)
        # elif(key == 'search_content'):
        #     keyword = request.meta.get("keyword")
        #     url = request.url
        #
        #     control = driver_control()
        #     content = control.get_driver_page_source(url)
        #
        #     return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        # elif(key == 'search_people'):
        #     keyword = request.meta.get("keyword")
        #     url = request.url
        #
        #     control = driver_control()
        #     content = control.get_driver_page_source(url)
        #     control.get_more()
        #     content = control.get_more_page_source()
        #     return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        # elif (key == 'search_post'):
        #     url = request.url
        #
        #     control = driver_control()
        #     content = control.get_driver_page_source(url)
        #     return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        # elif key == 'search_question':
        #     url = request.url
        #     control = driver_control()
        #     content = control.get_driver_page_source(url)
        #     return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        # elif key == 'search_people_by_content':
        #     url = request.url
        #     control = driver_control()
        #     content = control.get_driver_page_source(url)
        #     return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        if key == 'to_content':
            token = self.token
            url=request.url
            fields = 'text'
            params = {
                'token': token,
                'url': url,
                'fields': fields
            }

            result = requests.get('http://api.url2io.com/article', params=params)
            content = result.json()

            content['time'] = request.meta.get('time')

            return Response(url=request.url, body=json.dumps(content, ensure_ascii=False).encode(encoding='utf-8'),
                            request=request)

        else:
            def get_ua():
                return getattr(self.ua, self.ua_type)

            # print(get_ua())
            request.headers.setdefault('User-Agent', get_ua())

            thisip = random.choice(IPPOOL)
            proxy = thisip
            protocol = 'https' if 'https' in proxy else 'http'
            proxies = {protocol: proxy}
            try:
                if requests.get('https://www.iteye.com/', proxies=proxies,timeout=15).status_code != 200:
                    IPPOOL.remove(thisip)
                    return None
            except:
                IPPOOL.remove(thisip)
                print("%s removed"%thisip)
                return None

            # protocol = 'https' if 'https' in thisip else 'http'
            # print("this is ip:" + thisip)
            request.meta["proxy"] = thisip
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # stat=response.status
        # if stat==401:
        #     time

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
