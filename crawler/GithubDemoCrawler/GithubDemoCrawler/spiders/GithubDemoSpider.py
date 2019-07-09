import scrapy
import json
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from ..driver import github_driver

class GithubDemoSpider(scrapy.Spider):
    name = 'github-spider'

    def __init__(self):
        super(GithubDemoSpider, self).__init__()

        with open('config.json', 'r') as cursor:
            self.CONFIG = json.load(cursor)

        dispatcher.connect(self.SpiderStopped, signals.engine_stopped)

    def SpiderStopped(self):
        for driver in github_driver.driver_pools:
            driver.close()

    def start_requests(self):
        pass