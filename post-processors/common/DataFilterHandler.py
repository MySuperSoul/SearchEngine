from common.Config import MongoConfig

class DataFilterHandler():
    def __init__(self, database_name, collection_name):
        self.mongo_config = MongoConfig(database_name=database_name, collection_name=collection_name)
        self.collection_cursor = self.mongo_config.GetMongoCursor()

    # filter with distinct url
    def start(self):
        cursor = self.collection_cursor
        urls_list = cursor.distinct('url')

        for url in urls_list:
            num = cursor.count({"url" : url})
            for i in range(1, num):
                cursor.remove({"url" : url}, 0)

        self.mongo_config.CloseConnection()
        print('Data filter done.')
