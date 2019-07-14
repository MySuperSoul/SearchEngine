from common.Config import MongoConfig

if __name__ == '__main__':
    config = MongoConfig(database_name='TechHub', collection_name='Bilibili')
    cursor = config.GetMongoCursor()
    count = 0

    for document in cursor.find():
        url = document['url']
        new_time = document['date'].split()[0]
        cursor.update_one({'url' : url}, {'$set' : {'date' : new_time}})
        count += 1
        print('Finish update document {}'.format(count))

    config.CloseConnection()
