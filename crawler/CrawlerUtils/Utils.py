import requests
import json
from lxml import etree

class Utils():
    @classmethod
    def GetPageContent(cls, token, url):
        fields = ','.join(['text', ])
        params = {
            'token': token,
            'url': url,
            'fields': fields
        }

        result = requests.get('http://api.url2io.com/article', params=params)
        content = result.json()
        return content

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