from common.Config import MongoConfig
from common.SimHash import SimHashFilter

class DataFilterHandler():
    def __init__(self, database_name, collection_name, use_localhost=False):
        self.mongo_config = MongoConfig(database_name=database_name, collection_name=collection_name, use_localhost=use_localhost)
        self.collection_cursor = self.mongo_config.GetMongoCursor()
        self.similarity_filter = SimHashFilter(128)
        self.count = 0
        self.code_list = []

    # filter with distinct url and similarity
    def start(self):
        cursor = self.collection_cursor
        url_set = set()

        for document in cursor.find():
            url = document['url']
            content = document['content']

            # first filter same url
            if url in url_set and len(url_set) != 0:
                cursor.remove({"url" : url})
                print('Duplicate url for {}'.format(url))
                continue

            url_set.add(url)

            # then filter similarity threshold
            self.FilterSimilarity(cursor, url, content)

        self.mongo_config.CloseConnection()
        print('Data filter done.')

    def FilterSimilarity(self, cursor, url, content):
        valid_flag = True

        code = self.similarity_filter.GetCodeForText(text=content)
        if len(self.code_list) == 0:
            self.code_list.append(code)
        else:
            list_length = len(self.code_list)
            for index in range(list_length):
                c = self.code_list[index]
                (similar, similarity) = self.similarity_filter.IsSimilarByCode(c, code)
                if similar == True:
                    cursor.remove({"url" : url})
                    print('Delete document for {}, similarity is {}'.format(
                        url, similarity
                    ))
                    valid_flag = False
                    break
                else:
                    continue

            if valid_flag == True:
                print('Valid document for position: {}'.format(self.count))
                self.code_list.append(code)

        self.count += 1