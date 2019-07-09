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
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.driver_option.add_experimental_option("prefs", prefs)
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



# import threading
# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#
# thread_control = False
# driver_pools = []
# driver_produce_lock = threading.Lock()
#
# # dcap = dict(DesiredCapabilities.PHANTOMJS)
# # dcap["phantomjs.page.settings.loadImages"] = False  # not to load images
# # driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=r'phantomjs.exe')
#
# chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)
# driver=webdriver.Chrome(chrome_options=chrome_options)
#
# class driver_control():
#     def get_usable_driver(self, url):
#         global driver
#         control_mode = False
#         while(control_mode == False):
#             try:
#                 driver.get(url)
#                 control_mode = True
#             except:
#                 driver.quit()
#                 driver=webdriver.Chrome()
#                 # driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=r'phantomjs.exe')
#                 driver.implicitly_wait(1)
#                 continue
#
#     def get_driver_page_source(self, url):
#         global driver
#         self.get_usable_driver(url)
#         driver.execute_script("window.scrollTo(0, 100000)")
#         driver.implicitly_wait(1)
#         return driver.page_source
#
#     def get_more(self):
#         global driver
#         try:  # maybe some do not have more information
#             driver.find_elements_by_xpath('//button[@class="Button ProfileHeader-expandButton Button--plain"]')[0].click()  # get more information
#         except Exception as e:
#             return
#
#     def get_more_page_source(self):
#         global driver
#         return driver.page_source
#
