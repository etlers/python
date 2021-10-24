import pandas as pd
import time
import date_util as DU


def make_dic_jongmok_list():
    df_jongmok = pd.read_csv("./csv/jongmok_list.csv", encoding="cp949")
    df_jongmok = df_jongmok[["한글 종목약명","단축코드"]]
    dict_jongmok = {}
    for key, row in df_jongmok.iterrows():
        dict_jongmok[row["한글 종목약명"]] = row["단축코드"]

    return dict_jongmok

# 데이터 타입에 맞게 재생성
def remake_list(list_base, num_cols, rate_cols):    
    for idx in range(len(num_cols)):
        try:
            num = int(list_base[num_cols[idx]].replace(",",""))
        except:
            num = 0
        list_base[num_cols[idx]] = num
    for idx in range(len(rate_cols)):
        try:
            num = float(list_base[rate_cols[idx]].replace(",","").replace("%",""))
        except:
            num = 0
        list_base[rate_cols[idx]] = num
        
    return list_base

# 오른쪽에 문자열 채우기
def rpad(i, width, fillchar='0'):
    return str(i).ljust(width, fillchar)

# 지정한 시간만큼 메세지 뿌리며 대기
def waiting_seconds(sec, msg):
    idx = 0
    while True:
        idx += 1
        if idx > sec: break
        print(DU.get_now_datetime_string() + " ] ", msg)
        time.sleep(1)    