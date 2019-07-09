from ..drivers import *
from ..items import *
from scrapy.http import Request

class MyiteyeSpider(scrapy.Spider):
    name = "myiteye"
    allowed_domains = ["iteye.com"]
    start_urls = [
        "https://www.iteye.com/blogs",
        "https://www.iteye.com/blogs/category/os",
        "https://www.iteye.com/blogs/category/database",
        "https://www.iteye.com/blogs/category/language",
        "https://www.iteye.com/blogs/category/internet",
        "https://www.iteye.com/blogs/category/opensource",
        "https://www.iteye.com/blogs/category/industry",
        "https://www.iteye.com/blogs/category/develop",
    ]
    baseurl="https://www.iteye.com%s"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url=self.start_urls[0]
        yield Request(url, callback=self.parse_catalog ,headers=self.headers)

    # def parse(self, response):
    #      for sel in response.xpath('//ul/li'):
    #         item = BackItem()
    #         item['title'] = sel.xpath('a/text()').extract()
    #         item['link'] = sel.xpath('a/@href').extract()
    #         item['desc'] = sel.xpath('text()').extract()
    #         yield item

    def parse_catalog(self,response):
        catalogmenu=response.css('div[class*=nav_side] ul li a::attr(href)')
        # print(catalogmenu.extract())
        for r in catalogmenu.extract():
            url=self.baseurl%r
            yield Request(url=url,headers=self.headers)

    def parse(self,response):
        itemmenu = response.css('div[class*="blog clearfix"] ')
        # print(itemmenu.extract())
        for r in itemmenu:
            url=r.css('h3 a::attr(href)').extract_first()

            time=r.css('div[class*=blog_info] span[class*=date]::text').extract_first()
            yield Request(url=url,callback=self.parse_content,headers=self.headers,meta={
                "time":time
            })

        nexturl=response.css('a[class*="next_page"]::attr(href)').extract_first()
        if nexturl:
            url=self.baseurl%nexturl
            yield Request(url=url, headers=self.headers)

    def parse_content(self,response):
        item=DemoSpiderItem()
        item['url']=response.url
        item['title']=response.css('div[class*=blog_title] h3 a::text').extract_first()
        item['content']=response.xpath('//div[@id="blog_content"]').xpath('string(.)').extract_first()
        item['tags']=response.css('ul[class*=blog_categories] li a::text').extract()
        item['author']=response.css('div[id*=blog_owner_name]::text').extract_first()
        item['source']="Iteye"
        item['catalog']=2
        item['date']=response.css('div[class*=blog_bottom] ul li::text').extract_first()
        yield item
        # print(catalogmenu.extract())

