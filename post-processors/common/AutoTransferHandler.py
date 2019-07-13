from common.Config import MongoConfig

'''
This class is used for transfer documents from one collection to another.
Usage:
    handler = AutoTransferHandler(db, collection_from, collection_to)
    handler.start()
'''

class AutoTransferHandler():
    def __init__(self, database_name, collection_name_from, collection_name_to):
        self.config_from = MongoConfig(database_name=database_name, collection_name=collection_name_from, use_localhost=False)
        self.config_to = MongoConfig(database_name=database_name, collection_name=collection_name_to, use_localhost=False)
        self.cursor_from = self.config_from.GetMongoCursor()
        self.cursor_to = self.config_to.GetMongoCursor()
        self.count = 0

    def start(self):
        print('Transfer Begin')
        for document in self.cursor_from.find():
            self.cursor_to.insert_one(document)
            self.count += 1
            print('Insert success document {}'.format(self.count))
        print('Transfer Done.')

        self.config_from.CloseConnection()
        self.config_to.CloseConnection()
