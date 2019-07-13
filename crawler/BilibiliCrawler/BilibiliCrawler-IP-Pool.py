import requests
from lxml import etree
import time
import pymongo
import threading
import random
import GetIP

start_url = 'https://search.bilibili.com/video?keyword={0}&page={1}'

headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Connection": "close"
           }

connection = pymongo.MongoClient('mongodb://49.234.90.146:37017,49.234.90.146:47017,49.234.90.146:57017')
db = connection["TechHub"]
collection = db["Bilibili"]


def LoadUserAgents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
    random.shuffle(uas)
    return uas


uas = LoadUserAgents("./user_agents.txt")


# 根据url得到html
def get_html(url):
    ua = random.choice(uas)
    headers["user-agent"] = ua
    retry = 5
    while retry > 0:
        time.sleep(3)
        try:
            res = requests.get(url, headers=headers)
            print(res.text)
        except Exception as e:
            print(e)
            retry = retry - 1
            time.sleep(1)
            continue

        if res.status_code == 200:
            return res.text
        else:
            retry = retry - 1
            time.sleep(1)

    return ""


# 根据url、key得到页面内容
def parse_content(url, key):
    global ip_thread
    tmp_html = ip_thread.get_html(url)
    if tmp_html == "":
        print("parse_content error")
        return

    try:
        etree_tmp = etree.HTML(tmp_html)
        item = {}
        item["url"] = url
        item["catalog"] = 4
        item["title"] = etree_tmp.xpath('//h1/span')[0].text
        item["content"] = ""
        item["source"] = "Bilibili"
        item["date"] = etree_tmp.xpath('//div[@class="video-data"]')[0].xpath('./span')[1].text
        item["summary"] = ""
        item["author"] = etree_tmp.xpath('//a[contains(@class,"username")]')[0].text
        item["tags"] = []
        for i in etree_tmp.xpath('//li[@class="tag"]/a'):
            item["tags"].append(i.text)
    except Exception as e:
        print(e)
        print("解析最后: " + url)
        return

    collection.insert_one(document=item)
    retry = 5
    while retry > 0:
        try:
            collection.insert_one(document=item)
            print("ok")
            return
        except Exception as e:
            time.sleep(3)
            retry = retry - 1
    else:
        print("mongodb 插入超时")
        return


# 每页爬下文章链接，返回这页的文章链接
def parse_page_url(url):
    result = []
    global ip_thread
    html = ip_thread.get_html(url)
    if html == "":
        print("error in parse_page_url: " + url)
        return result

    html = etree.HTML(html)
    a_list = html.xpath('//li[@class="video matrix"]/a')
    for a in a_list:
        result.append("https:" + a.xpath('./@href')[0])
    return result


# 得到一共的页数，并且调用 parse_page_url，返回所有文章的链接
def parse_page(url, key):
    result = []
    print("start in total page: " + key + " " + url)

    tmp_result = parse_page_url(url)
    if len(tmp_result) == 0:
        print("parse_page 一开始就错误: " + url)
        return result

    result.append((key, tmp_result))  # 第一页的结果加进去

    try:
        global ip_thread
        html = ip_thread.get_html(url)
        if html == "":
            print("error in parse_page: " + url)
            return result
        html = etree.HTML(html)
        total_page = int(html.xpath('//button[@class="pagination-btn"]')[0].text)
    except Exception as e:
        print("在得到total page的时候发生错误: " + url)
        return result

    for i in range(2, total_page + 1):
        tmp_url = start_url.format(key, i)
        tmp_result = parse_page_url(tmp_url)
        result.append((key, tmp_result))  # 每页一个元组 (key, [url,])

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
            self.url_list.extend(result)
            self.lock.release()
            print("crawl done")


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
                print("parse done")
                break
            else:
                target = self.url_list.pop()
                if len(target) == 0:
                    self.lock.release()
                    continue
                key = target[0]
                articles = target[1]
                for article in articles:
                    parse_content(article, key)
                self.lock.release()
                time.sleep(1)


def main(key_list):
    url_list = []
    lock = threading.Lock()

    i = 0
    step = 4
    while i < len(key_list):
        last = min(i + step, len(key_list))
        page_thread = []
        for j in range(i, last):
            thread = ThreadCrawl(start_url.format(key_list[j], 1), key_list[j], url_list, lock)
            thread.start()
            page_thread.append(thread)

        for thread in page_thread:
            thread.join()

        i = i + step

    print(len(url_list))

    parse_thread = []
    for i in range(4):
        thread = ThreadParse(url_list, lock)
        thread.start()
        parse_thread.append(thread)

    for thread in parse_thread:
        thread.join()

    global ip_thread
    ip_thread.stop()
    ip_thread.join()
    connection.close()
    print("done")


if __name__ == "__main__":
    global ip_thread
    ip_thread = GetIP.IPCrawler(16)
    ip_thread.start()
    time.sleep(30)

    key_list = ["Spring Cloud Config", "Spring Cloud Bus", "Eureka", "Hystrix", "Zuul", "Archaius", "Consul", "Spring Cloud for Cloud Foundry", "Spring Cloud Sleuth", "Spring Cloud Data Flow", "Spring Cloud Security", "Spring Cloud Zookeeper", "Spring Cloud Stream", "Spring Cloud CLI", "Ribbon", "Turbine", "Feign", "Spring Cloud Task", "Spring Cloud Connectors", "Spring Cloud Cluster", "Spring Cloud Starters"]
    sec_key_list = ["maven", "MySQL","Spring Boot", "Spring Security", "Spring Session", "MongoDB","Redis","RESTful API","OAuth","Token Authentication","JWT","RabbitMQ","Solr","Elasitic search","docker","docker-compose","k8s","Apache","Nginx","Tomcat","Websockets","GraphQL","Neo4j","OrientDB"]
    key_list.extend(sec_key_list)
    main(key_list)
