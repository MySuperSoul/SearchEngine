from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import InvalidSessionIdException
import random
import time

class CrawlerBaseDriver():
    def __init__(self):
        self.delay_time = 1
        self.driver_pool_number = 1
        self.driver_option = Options()
        self.driver_option.add_argument('--headless')
        self.driver_option.add_argument('--no-sandbox')
        self.driver_option.add_argument('--window-size=1420,1080')
        self.driver_option.add_argument('--disable-gpu')

        prefs = {"profile.managed_default_content_settings.images": 2}
        self.driver_option.add_experimental_option("prefs", prefs)
        self.driver_pools = []

        for i in range(self.driver_pool_number):
            self.driver_pools.append(webdriver.Chrome(chrome_options=self.driver_option))

    def GenerateNewDriver(self):
        return webdriver.Chrome(chrome_options=self.driver_option)

    def GetValidDriverForPage(self, url, key):
        random_pos = random.randint(0, self.driver_pool_number - 1)
        random_driver = self.driver_pools[random_pos]

        control_mode = False
        while control_mode == False:
            try:
                random_driver.get(url)
                self.driver_pools[random_pos] = random_driver

                control_mode = True
                return random_driver

            except InvalidSessionIdException as e:
                time.sleep(0.5)
                continue

            except Exception as e:
                random_driver.close()
                random_driver = self.GenerateNewDriver()
                random_driver.implicitly_wait(1)
                continue