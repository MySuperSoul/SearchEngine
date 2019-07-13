from common.DataFilterHandler import DataFilterHandler
from common.Config import MongoConfig
from zhihu.AutoSummaryHandler import AutoSummaryHandler
from common.AutoTransferHandler import AutoTransferHandler

def Summary():
    config = MongoConfig(database_name='TechHub', collection_name='zhihu', use_localhost=False)
    cursor = config.GetMongoCursor()
    summary_handler = AutoSummaryHandler()
    count = 0

    for document in cursor.find():
        content = document['content']
        url = document['url']
        if len(content) < 10:
            cursor.delete_one({"url": url})
            print('Remove too short document')
        else:
            summary = summary_handler.GetSummary(content=content)
            cursor.update_one({'url': url}, {'$set': {'summary': summary}})
            print('Finish summary for document {}'.format(count))
        count += 1

    # release resources
    config.CloseConnection()

def Transfer():
    handler = AutoTransferHandler(database_name='TechHub', collection_name_from='zhihu', collection_name_to='infos')
    handler.start()

if __name__ == '__main__':
    # first filter the data
    # filter = DataFilterHandler(database_name='TechHub', collection_name='zhihu', use_localhost=False)
    # filter.start()

    # Then auto summary the content
    # Summary()

    # Transfer data
    Transfer()