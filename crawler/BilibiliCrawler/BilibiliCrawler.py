import requests
from lxml import etree
import time
import pymongo
import threading

start_url = 'https://search.bilibili.com/video?keyword={0}&page={1}'

headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "cookie": "JSESSIONID=F8C1DBC20DB11E6A1FEF9AFDDB23EBC8; uuid_tt_dd=10_30805606620-1562635550070-577900; dc_session_id=10_1562635550070.803803",
            "upgrade-insecure-requests": "1",
            "pragma": "no-cache",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
           }

connection = pymongo.MongoClient('mongodb://49.234.90.146:37017,49.234.90.146:47017,49.234.90.146:57017', connect=False)
db = connection["TechHub"]
collection = db["cx"]


# 根据url得到html
def get_html(url):
    html = requests.get(url, headers=headers).text
    return html


# 根据url、key得到页面内容
def parse_content(url, key):
    token = "FOGuPOBcR-eNuQ-U4SB5-w"
    fields = ','.join(['text', ])
    params = {
        'token': token,
        'url': url,
        'fields': fields
    }
    result = requests.get('http://api.url2io.com/article', params=params)
    result = result.json()

    item = {}
    item["url"] = url
    item["catalog"] = 4
    item["title"] = result["title"]
    item["content"] = result["text"]
    item["source"] = "Bilibili"
    item["date"] = result["date"]

    item["summary"] = ""
    item["author"] = etree.HTML(get_html(url)).xpath('//a[@class="username"]')[0].text
    item["tags"] = [key, ]

    collection.insert_one(document=item)


# 每页爬下文章链接，返回这页的文章链接
def parse_page_url(url):
    html = get_html(url)
    html = etree.HTML(html)
    a_list = html.xpath('//li[@class="video matrix"]/a')
    result = []
    for a in a_list:
        result.append("https:" + a.xpath('./@href')[0])
    return result


# 得到一共的页数，并且调用 parse_page_url，返回所有文章的链接
def parse_page(url, key):
    result = []
    html = get_html(url)
    html = etree.HTML(html)
    total_page = int(html.xpath('//button[@class="pagination-btn"]')[0].text)
    for i in range(1, total_page + 1):
        url = start_url.format(key, i)
        tmp_result = parse_page_url(url)
        result.append((key, tmp_result))  # 每页一个元组 (key, [url,])
        time.sleep(0.5)

    return result


class ThreadCrawl(threading.Thread):
    def __init__(self, url, key, url_list, lock):
        super(ThreadCrawl, self).__init__()
        self.url = url
        self.key = key
        self.url_list = url_list
        self.lock = lock

    def run(self):
        print("ThreadCrawl Start: " + self.key)
        result = parse_page(self.url, self.key)

        if self.lock.acquire():
            self.url_list.append(result)
            self.lock.release()


class ThreadParse(threading.Thread):
    def __init__(self, url_list, lock):
        super(ThreadParse, self).__init__()
        self.url_list = url_list
        self.lock = lock

    def run(self):
        print("ThreadParse Start")

        while self.lock.acquire():
            if len(self.url_list) == 0:
                self.lock.release()
                break
            else:
                target = self.url_list.pop()
                key = target[0]
                articles = target[1]
                for article in articles:
                    parse_page(article, key)
                self.lock.release()
                time.sleep(0.5)


def main(key_list):
    url_list = []
    lock = threading.Lock()

    page_thread = []
    for key in key_list:
        thread = ThreadCrawl(start_url.format(key, 1), key, url_list, lock)
        thread.start()
        page_thread.append(thread)

    for thread in page_thread:
        thread.join()

    parse_thread = []
    for i in range(10):
        thread = ThreadParse(url_list, lock)
        parse_thread.append(thread)

    for thread in parse_thread:
        thread.join()


if __name__ == "__main__":
    key_list = ["Spring Cloud"]
    main(key_list)
    # parse_content(url, "Spring cloud")
    # parse_page_url(url)
    # result = parse_page(get_html(url), "Spring+cloud")
    # print(len(result))
    # url = "https://www.bilibili.com/video/av56799177?from=search&seid=865120776882731184"
    # key = "spring cloud"
    # parse_content(url, "Spring cloud")
