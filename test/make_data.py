import sys

sys.path.append("C:/Users/etlers/Documents/project/python/common")

import date_util as DU
import conn_db as DB

list_dt = DU.get_datetime_list_between("2020-05-01 21:00:00", "2021-08-20 21:00:00", 1 * 60 * 24)

desc_head = """
ALTER TABLE pt_tbl
PARTITION BY RANGE (DT)
(
"""
desc_body = ""

for dt in list_dt:
    qry = f"""insert into pt_tbl
        select '{DU.get_datetime_string(dt)}', JONGMOK_CD, JONGMOK_NM, ARTICLE, POS_CNT, NEG_CNT, END_PRC, END_PRC_INC, HIGH_RT, HIGH_PRC, LOW_PRC, LOW_GAP, VOL
          from naver_news"""
    DB.transaction_data(qry)
#     dt_str = DU.get_datetime_string(dt).split(" ")[0].replace("-","")
#     dt_next = DU.get_before_datetime(DU.get_datetime_string(dt), days=-1)
#     desc_body += f"""PARTITION p{dt_str} VALUES LESS THAN (unix_timestamp('{dt_next}')) ENGINE = INNODB, \n"""

# print(desc_head + desc_body)