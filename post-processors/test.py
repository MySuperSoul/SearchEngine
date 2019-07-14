import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from common.Config import MongoConfig
from pyhanlp import *
from snownlp import SnowNLP

tr4w = TextRank4Sentence()
config = MongoConfig(database_name='TechHub', collection_name='jianshu')
cursor = config.GetMongoCursor()

for document in cursor.find().limit(20):
    try:
        tr4w.analyze(text=document['content'], lower=True, source='all_filters')
        s = SnowNLP(document['content'])

        print('TextRank4Keyword: ', '. '.join(sen['sentence'] for sen in tr4w.get_key_sentences(num=2)))
        print('HanLP: ', HanLP.extractSummary(document['content'], 2))
        print('SnowNLP: ', s.summary(2))
        print()
        # content = str(document['content'])
        # position = content.find('\n\n')
        # if content[:position].isdigit():
        #     print(content[position + 2:])
    except Exception as e:
        print('No summary!')
        continue

config.CloseConnection()