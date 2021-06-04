"""
    예약에서 공통으로 사용하는 함수들
"""

import datetime

list_yoil = [
    "월", "화", "수", "목", "금", "토", "일"
]

def get_first_saturday_col_idx():
    week_day = datetime.datetime.today().weekday()
