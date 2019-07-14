import datetime

class TimeProcessHandler():
    def __init__(self):
        self.date_map = {
            'Jan' : '01',
            'Feb' : '02',
            'Mar' : '03',
            'Apr' : '04',
            'May' : '05',
            'Jun' : '06',
            'Jul' : '07',
            'Aug' : '08',
            'Sep' : '09',
            'Oct' : '10',
            'Nov' : '11',
            'Dec' : '12'
        }

    def GetType(self, time):
        time_list = str(time).split(' ')
        # 1 -> 8 days ago
        if time_list[0].isdigit() and time_list[1] == 'days':
            return 1
        elif time_list[0].isdigit() and time_list[1] == 'hours': # 8 hours ago
            return 2
        elif len(time_list) == 3:
            return 3
        elif len(time_list) == 4:
            return 4

    def process(self, time):
        current_time = datetime.datetime.now()
        type = self.GetType(time)

        if type == 1:
            day = int(time.split(' ')[0])
            delta = datetime.timedelta(days=day)
            new_time = current_time - delta
            new_time = new_time.strftime('%Y-%m-%d')
        elif type == 2:
            hours = int(time.split(' ')[0])
            delta = datetime.timedelta(hours=hours)
            new_time = current_time - delta
            new_time = new_time.strftime('%Y-%m-%d')
        elif type == 3:
            time_list = time.split(' ')
            month = self.date_map[time_list[1]]
            day = time_list[-1]
            if len(day == 0): day = '0' + day
            year = '2019'
            new_time = year + '-' + month + '-' + day
        elif type == 4:
            time_list = time.split(' ')
            month = self.date_map[time_list[1]]
            day = time_list[2].strip(',')
            if len(day == 0): day = '0' + day

            year = time_list[-1]
            new_time = year + '-' + month + '-' + day

        return new_time