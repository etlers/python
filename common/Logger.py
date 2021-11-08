import datetime
from datetime import datetime

class Logger:
    def __init__(self, service_name):
        self.service_name = service_name

    def get_now_string(self):
        return datetime.today().strftime('%Y-%m-%d %H:%M:%S.%s')

    def info(self, dic):
        log_string = '. '.join(list(map(lambda k : (k + '="' + dic[k] + '"'), dic.keys())))
        print('[' + self.get_now_string() + '] [' + self.service_name + '] INFO - ' + log_string)

    def error(self, dic):
        log_string = '. '.join(list(map(lambda k : (k + '="' + dic[k] + '"'), dic.keys())))
        print('[' + self.get_now_string() + '] [' + self.service_name + '] ERROR - ' + log_string)