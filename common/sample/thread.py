import threading
import time
import requests


class slack_message(threading.Thread):
    def __init__(self, message_string):
        super().__init__()
        self.message_string = message_string            # thread 이름 지정

    def run(self):
        url = "https://hooks.slack.com/services/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"
        payload = { "text" : self.message_string }
        requests.post(url, json=payload)


print("main thread start")
message_string = "slack message"
for i in range(5):
    name = "thread {}".format(i)
    t = slack_message(message_string + str(i))                # sub thread 생성
    t.start()                       # sub thread의 run 메서드를 호출

print("main thread end")