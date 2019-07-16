import requests
import json
from lxml import etree
import time
import random

class Utils():
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "upgrade-insecure-requests": "1",
        "pragma": "no-cache",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }

    USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"
    ]

    IP_LIST = [
        {'http' : 'http://27.43.187.242:9999'},
        {'http': 'http://120.83.109.57:9999'},
        {'http': 'http://117.91.132.116:9999'},
        {'http': 'http://114.239.199.144:9999'},
        {'http': 'http://1.197.204.94:9999'},
        {'http': 'http://42.238.84.20:9999'},
        {'http': 'http://222.89.32.186:9999'},
        {'http': 'http://121.233.207.94:9999'},
        {'https': 'https://210.22.176.146:32153'},
        {'https': 'https://115.219.105.201:8010'},
    ]

    @classmethod
    def GetPageContent(cls, token, url):
        retry_time = 5
        while retry_time >= 0:
            fields = ','.join(['text', ])
            params = {
                'token': token,
                'url': url,
                'fields': fields
            }

            result = requests.get('http://api.url2io.com/article', params=params)
            if result.status_code == 200:
                content = result.json()
                return content
            else:
                retry_time -= 1
        else:
            raise Exception('api error')


    @classmethod
    def GetResponseForJson(cls, content):
        body_content = json.dumps(content, ensure_ascii=False).encode(encoding='utf-8')
        return body_content

    @classmethod
    def GetSelectorForText(cls, content):
        selector = etree.HTML(content)
        return selector

    @classmethod
    def GetInfoDicFromBytes(cls, content):
        decode_content = bytes.decode(content, encoding='utf-8')
        info_dic = json.loads(decode_content)
        return info_dic

    @classmethod
    def FeedDocument(cls, document, info_dic):
        document['title'] = info_dic['title'],
        document['summary'] = info_dic['summary'],
        document['url'] = info_dic['url'],
        document['tags'] = info_dic['tags'],
        document['catalog'] = info_dic['catalog'],
        document['content'] = info_dic['text'].strip('\n'),
        document['source'] = info_dic['source'],
        document['date'] = info_dic['date'],
        document['author'] = info_dic['author']
        return document

    @classmethod
    def GetPageContentByRequests(cls, url):
        retry_time = 5
        while retry_time >= 0:
            cls.headers['user-agent'] = random.choice(cls.USER_AGENT_LIST)
            proxy = random.choice(cls.IP_LIST)

            html = requests.get(url=url, headers=cls.headers, proxies=proxy)
            if html.status_code != 200:
                time.sleep(1)
                retry_time -= 1
            else:
                return html.text
        else:
            raise Exception('Get error')