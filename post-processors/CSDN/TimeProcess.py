from common.Config import MongoConfig

if __name__ == '__main__':
    config = MongoConfig(database_name='TechHub', collection_name='CSDN')
    cursor = config.GetMongoCursor()
    count = 0

    for document in cursor.find():
        url = document['url']
        new_time = document['date'].split()[0]
        new_time = new_time.replace("年", "-")
        new_time = new_time.replace("月", "-")
        new_time = new_time.replace("日", "")
        if len(new_time) != 10:
            raise Exception("error")
        cursor.update_one({'url' : url}, {'$set' : {'date' : new_time}})
        count += 1
        print('Finish update document {}'.format(count))
    print("done")
    config.CloseConnection()
