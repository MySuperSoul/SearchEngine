from common.DataFilterHandler import DataFilterHandler
from stackoverflow.ContentProcessHandler import ContentProcessHandler
from stackoverflow.TimeProcessorHandler import TimeProcessHandler
from stackoverflow.AutoSummaryHandler import AutoSummaryHandler
from common.Config import MongoConfig

if __name__ == '__main__':
    # first filter the data
    # filter = DataFilterHandler(database_name='TechHub', collection_name='stackoverflow', use_localhost=False)
    # filter.start()

    content_handler = ContentProcessHandler()
    time_handler = TimeProcessHandler()
    summary_handler = AutoSummaryHandler()
    count = 0

    config = MongoConfig(database_name='TechHub', collection_name='stackoverflow')
    cursor = config.GetMongoCursor()

    for document in cursor.find():
        url = document['url']
        content = document['content']

        # process content
        (change, new_content) = content_handler.GetNewContent(content=content)

        # process time
        date = time_handler.process(document['date'])

        # process summary
        summary = summary_handler.GetSummary(new_content)

        if change == True:
            cursor.update_one({'url' : url}, {'$set': {'summary': summary, 'date' : date, 'content' : new_content}})
        else:
            cursor.update_one({'url' : url}, {'$set': {'summary': summary, 'date' : date}})

        print('Finish document {}'.format(count))
        count += 1

    config.CloseConnection()