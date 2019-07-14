from common.DataFilterHandler import DataFilterHandler
from jianshu.AutoSummaryHandler import AutoSummaryHandler
from jianshu.TimeProcessHandler import TimeProcessHandler
from common.Config import MongoConfig

if __name__ == '__main__':
    # first filter the data
    # filter = DataFilterHandler(database_name='TechHub', collection_name='jianshu', use_localhost=False)
    # filter.start()

    summary_handler = AutoSummaryHandler()
    time_handler = TimeProcessHandler()
    config = MongoConfig(database_name='TechHub', collection_name='jianshu')
    cursor = config.GetMongoCursor()
    count = 0

    for document in cursor.find({}, no_cursor_timeout=True):
        content = document['content']
        url = document['url']
        summary = summary_handler.GetSummary(content)

        new_time = time_handler.process(document['date'])
        cursor.update_one({'url' : url}, {'$set' : {'summary' : summary, 'date' : new_time}})
        print('Finish update document {}'.format(count))
        count += 1

    config.CloseConnection()
