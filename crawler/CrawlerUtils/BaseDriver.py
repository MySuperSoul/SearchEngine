from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class CrawlerBaseDriver():
    def __init__(self):
        self.delay_time = 1
        self.driver_pool_number = 2
        self.driver_option = Options()
        self.driver_option.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.driver_option.add_experimental_option("prefs", prefs)
        self.driver_pools = []

        for i in range(self.driver_pool_number):
            self.driver_pools.append(webdriver.Chrome(chrome_options=self.driver_option))

    def GenerateNewDriver(self):
        return webdriver.Chrome(chrome_options=self.driver_option)

    def GetValidDriverForPage(self, url, key):
        pass