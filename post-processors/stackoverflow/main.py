from common.DataFilterHandler import DataFilterHandler

if __name__ == '__main__':
    # first filter the data
    filter = DataFilterHandler(database_name='TechHub', collection_name='stackoverflow', use_localhost=False)
    filter.start()