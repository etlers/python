import requests
import yaml, time
import pyautogui as pg

# with open('./config/jongmok.yaml', encoding="utf-8-sig") as stream:
#     try:
#         dict_dt = yaml.safe_load(stream)
#         webhook_url = dict_dt['WEBHOOK_URL']
#     except yaml.YAMLError as exc:
#         print(exc)

def open_slack_page():
    pg.moveTo(664, 1065)
    time.sleep(0.5)
    pg.click()
    time.sleep(0.5)
    pg.write("https://etlers.slack.com/apps/A0F7XDUAZ-incoming-webhooks\n")
    time.sleep(0.5)

def send_message_to_slack(msg):
    # open_slack_page()
    msg = msg.replace('"', "'").replace("/","")
    url = "https://hooks.slack.com/services/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"
    payload = { "text" : msg } 
    response = requests.post(url, json=payload)
    print(response)