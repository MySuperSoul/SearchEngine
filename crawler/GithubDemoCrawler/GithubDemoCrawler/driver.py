from CrawlerUtils.BaseDriver import CrawlerBaseDriver
import random
import time

class GithubDriver(CrawlerBaseDriver):
    def __init__(self):
        super(GithubDriver, self).__init__()

    def GetValidDriverForPage(self, url, key):
        pass

github_driver = GithubDriver()