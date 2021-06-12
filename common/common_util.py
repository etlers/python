import pandas as pd


def make_dic_jongmok_list():
    df_jongmok = pd.read_csv("./csv/jongmok_list.csv", encoding="cp949")
    df_jongmok = df_jongmok[["한글 종목약명","단축코드"]]
    dict_jongmok = {}
    for key, row in df_jongmok.iterrows():
        dict_jongmok[row["한글 종목약명"]] = row["단축코드"]

    return dict_jongmok