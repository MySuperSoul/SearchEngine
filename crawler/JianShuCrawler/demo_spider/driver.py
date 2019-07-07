from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

class Driver():
    def __init__(self):
        self.delay_time = 2
        self.driver_pool_number = 3
        self.driver_option = Options()
        self.driver_option.add_argument('--headless')
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
                if key == 'page':
                    element = WebDriverWait(random_driver, 10, 0.5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'result'))
                    )
                random_driver.execute_script('window.scrollTo(0, 100000)')
                return random_driver

            except Exception as e:
                random_driver.quit()
                random_driver.close()
                random_driver = self.GenerateNewDriver()
                time.sleep(self.delay_time)
                continue

DemoDriver = Driver()