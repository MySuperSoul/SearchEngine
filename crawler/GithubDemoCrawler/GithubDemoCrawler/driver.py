from CrawlerUtils.BaseDriver import CrawlerBaseDriver

class GithubDriver(CrawlerBaseDriver):
    def __init__(self):
        super(GithubDriver, self).__init__()

github_driver = GithubDriver()