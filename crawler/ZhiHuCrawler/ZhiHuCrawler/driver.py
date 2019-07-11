from CrawlerUtils.BaseDriver import CrawlerBaseDriver
import random
import time

class ZhiHuDriver(CrawlerBaseDriver):
    def __init__(self):
        super(ZhiHuDriver, self).__init__()

    def GetValidDriverForPage(self, url, key):
        random_pos = random.randint(0, self.driver_pool_number - 1)
        random_driver = self.driver_pools[random_pos]

        control_mode = False
        while control_mode == False:
            try:
                random_driver.get(url)
                self.driver_pools[random_pos] = random_driver

                control_mode = True
                if key == 'page':
                    random_driver.execute_script("window.scrollBy(0,40000)")
                    time.sleep(self.delay_time)
                    random_driver.execute_script("window.scrollBy(0,80000)")
                    time.sleep(self.delay_time)
                    random_driver.execute_script("window.scrollBy(0,120000)")
                    time.sleep(self.delay_time)
                return random_driver

            except Exception as e:
                random_driver.close()
                random_driver = self.GenerateNewDriver()
                random_driver.implicitly_wait(1)
                continue

zhihu_driver = ZhiHuDriver()