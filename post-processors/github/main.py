from common.DataFilterHandler import DataFilterHandler
from common.Config import MongoConfig
from github.TimeProcessHandler import TimeProcessHandler

if __name__ == '__main__':
    # first filter the data
    # filter = DataFilterHandler(database_name='TechHub', collection_name='github', use_localhost=False)
    # filter.start()

    config = MongoConfig(database_name='TechHub', collection_name='github')
    cursor = config.GetMongoCursor()
    handler = TimeProcessHandler()

    for document in cursor.find().limit(10):
        date = document['date']
        print(handler.process(date))

    config.CloseConnection()