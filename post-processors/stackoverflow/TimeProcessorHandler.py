class TimeProcessHandler():
    def __init__(self):
        pass

    def process(self, time):
        time = str(time)
        if len(time) == 0: return

        new_time = time.split(' ')[0]
        return new_time