import pymongo

class MongoConfig():
    def __init__(self, database_name, collection_name, use_localhost=False):
        self.host = '49.234.90.146'
        self.port_1 = 37017
        self.port_2 = 47017
        self.port_3 = 57017
        self.database_name = database_name
        self.collection_name = collection_name
        self.use_localhost = use_localhost

    def GetMongoCursor(self):
        if self.use_localhost == False:
            mongo_url = 'mongodb://{}:{},{}:{},{}:{}'.format(
                self.host, self.port_1,
                self.host, self.port_2,
                self.host, self.port_3
            )
        else:
            mongo_url = 'mongodb://localhost:27017'

        self.client = pymongo.MongoClient(mongo_url)
        db = self.client[self.database_name]
        mongo_collection = db[self.collection_name]
        return mongo_collection

    def CloseConnection(self):
        self.client.close()