import requests
import json
from lxml import etree

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
        html = requests.get(url=url, headers=cls.headers)
        return html.text