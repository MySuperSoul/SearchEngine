from common.DataFilterHandler import DataFilterHandler
from common.Config import MongoConfig
from github.TimeProcessHandler import TimeProcessHandler
from common.AutoTransferHandler import AutoTransferHandler

if __name__ == '__main__':
    # first filter the data
    # filter = DataFilterHandler(database_name='TechHub', collection_name='github', use_localhost=False)
    # filter.start()

    # config = MongoConfig(database_name='TechHub', collection_name='github')
    # cursor = config.GetMongoCursor()
    # handler = TimeProcessHandler()
    # count = 0
    #
    # for document in cursor.find():
    #     url = document['url']
    #     date = document['date']
    #     new_date = handler.process(time=date)
    #     cursor.update_one({'url' : url}, {'$set': {'date' : new_date}})
    #     print('Update for {}, {}'.format(url, count))
    #     count += 1
    #
    # config.CloseConnection()

    handler = AutoTransferHandler(database_name='TechHub', collection_name_from='github',
                                  collection_name_to='infos')
    handler.start()