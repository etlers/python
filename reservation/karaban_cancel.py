"""
    취소된 카라반 예약을 찾아서 예약
"""
from ntpath import join
from selenium import webdriver
import time, datetime
import argparse, sys, os

sys.path.append("C:/Users/etlers/Documents/project/python/common")

import date_util as DU

selenium_dir = "../chromedriver/"
driver = webdriver.Chrome(selenium_dir + "chromedriver.exe")
url = 'http://imjingakcamping.co.kr/resv/res_01.html'
driver.get(url)

# 프로그램 메세지
pgm_msg = """
# 임진각 평화누리 캠핑장 카라반 지정한 일자에 취소한 자리 찾아서 예약하기
"""
print(pgm_msg)

list_args = []
# 요일 인덱스
dict_yoil = {
    1: "일", 
    2: "월", 
    3: "화", 
    4: "수", 
    5: "목", 
    6: "금", 
    7: "토",
}
# 존에 대한 번호. xpath 배열 번호에 사용됨
dict_zone_info = {
    "A": ["8", 14],
    "B": ["9", 15],
    "C": ["10", 9],
}


def reservation_click():
    # 예약정보 입력
    def send_resv_info(xpath_value, text_value):
        find = None
        
        while find == None:
            try:
                find = driver.find_element_by_xpath(xpath_value)
            except:
                time.sleep(0.1)
        find.clear()  # 글자 지움
        find.send_keys(text_value) # 글자 입력

    # 대인 4명 선택
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[9]/form/div[1]/div/table/tbody/tr[1]/td[4]/select/option[5]").click()
            print("인원 선택")
            break
        except:
            time.sleep(0.1)
    
    # 예약하기
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[9]/div[2]/button").click()
            print("예약하기 클릭")
            break
        except:
            time.sleep(0.1)
    
    # 예약정보
    send_resv_info("/html/body/div[4]/div[5]/div/form/fieldset/div/dl[1]/dd[1]/input", "최주용")
    send_resv_info("/html/body/div[4]/div[5]/div/form/fieldset/div/dl[1]/dd[2]/input", "010-5000-6104")
    send_resv_info("/html/body/div[4]/div[5]/div/form/fieldset/div/dl[2]/dd/input", "cazoobong@naver.com")
    send_resv_info("/html/body/div[4]/div[5]/div/form/fieldset/div/dl[3]/dd/input", "721005")
    send_resv_info("/html/body/div[4]/div[5]/div/form/fieldset/div/dl[4]/dd/input", "22노3140")
    print("정보전송 완료")
    # 약관
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[5]/div/form/div[12]/label").click()
            break
        except:
            time.sleep(0.1)
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[5]/div/form/div[14]/label").click()
            break
        except:
            time.sleep(0.1)
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[5]/div/form/div[15]/label").click()
            break
        except:
            time.sleep(0.1)
    # 예약하기
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[5]/div/form/div[16]/button").click()            
            break
        except:
            time.sleep(0.1)

# 존을 받아서 빈자리 확인하고 선택까지 함
def click_empty_position(zone_cd):
    # 자리 클릭을 못한 경우
    click_tf = False
    zone_num = dict_zone_info[zone_cd][0]
    # 전체 개수를 돌면서 빈자리가 있는지 확인
    for pos in range(dict_zone_info[zone_cd][1]):
        # 마감이 있으면 지나감
        try:
            magam = driver.find_element_by_xpath(f"/html/body/div[4]/div[1]/div/div[8]/div[{int(zone_num)+1}]/div[{pos+1}]/span").text
        except:
            magam = "NO"
        # 마감이 아닌 경우 클릭
        if magam == "NO":
            driver.find_element_by_xpath(f'/html/body/div[4]/div[1]/div/div[8]/div[{int(zone_num)+1}]/div[{pos+1}]/label').click()
            click_tf = True
            break

    return click_tf

# 
def click_zone(zone_cd):
    click_tf = False
    # 유의사항 체크
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[7]/label").click()
            break
        except:
            time.sleep(0.1)
    # 존 명칭이 나올 때까지 대기
    zone_num = dict_zone_info[zone_cd][0]
    zone_path = f'/html/body/div[4]/div[1]/div/div[8]/div[1]/button[{zone_num}]'
    while True:
        try:
            zone_nm = driver.find_element_by_xpath(zone_path).text
            print(zone_nm)
            break                
        except:
            time.sleep(0.1)
    # 존 클릭
    driver.find_element_by_xpath(zone_path).click()

    click_tf = click_empty_position(zone_cd)

    return click_tf


# 예약 시작을 위한 사전 준비
def prepare_for_reservation():

    selected_tf = False

    # 사이트의 남은 자리 확인
    def site_count():
        while True:
            try:
                empty_cnt_a = int(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[4]/table/tbody/tr/td[7]/span').text)
                empty_cnt_b = int(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[4]/table/tbody/tr/td[8]/span').text)
                empty_cnt_c = int(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[4]/table/tbody/tr/td[9]/span').text)
                break
            except:
                time.sleep(0.1)

        return empty_cnt_a, empty_cnt_b, empty_cnt_c
    
    # 예약하기 버튼이 생성됐는지 확인. 있다면 화면이 떴다는 의미
    while True:
        try:
            rsv_btn = driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[9]/div[2]/button").text
            time.sleep(0.1)
            break
        except:
            time.sleep(0.5)                
    
    # 주, 요일 설정
    week_num = list_args[0] + 1
    day_col_num = list_args[1]
    # 달력의 일자 가져오기
    while True:
        try:
            calendar_day = driver.find_element_by_xpath(f"/html/body/div[4]/div[1]/div/div[3]/div[2]/div[{week_num}]/span[{day_col_num}]/a").text
            break
        except:
            time.sleep(0.1)
    
    # 가져온 달력 일자를 선택
    while True:
        try:
            driver.find_element_by_xpath(f"/html/body/div[4]/div[1]/div/div[3]/div[2]/div[{week_num}]/span[{day_col_num}]/a").click()
            break
        except:
            time.sleep(0.1)

    # 제대로 일자 선택이 됐다면 사이트 빈자리 추출
    empty_cnt_a, empty_cnt_b, empty_cnt_c = site_count()
    # 빈자리가 없는 경우
    if empty_cnt_a + empty_cnt_b + empty_cnt_c == 0:
        print("빈자리가 없습니다.", end=" ")
        return False
    # 빈자리에 따른 존
    if empty_cnt_a > 0:
        selected_tf = click_zone("A")
    elif empty_cnt_b > 0:
        selected_tf = click_zone("B")
    elif empty_cnt_c > 0:
        selected_tf = click_zone("C")

    return selected_tf


# 최초 팝업을 클릭해서 없애고 예약을 위한 사이트 체크로 들어감
def execute():
    # 팝업 확인. 없을 수도 있음
    try:
        driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/form/div/span/a').click()
    except:
        time.sleep(0.1)
    # 예약 사전 준비 및 사이트 확인
    while True:
        if prepare_for_reservation():
            reservation_click()
            break
        else:
            print(DU.get_now_datetime_string())
            time.sleep(1)
    
    # driver.close()


if __name__ == "__main__":
    # 프로그램에서 예약할 사이트 인자 받아오기
    parser = argparse.ArgumentParser(description='Karaban Site Argument. A, B, C')
    parser.add_argument('--week', type=int, help='2 ~ 7')
    parser.add_argument('--yoil', type=int, help='Sun ... Sat: 1 ~ 7')
    args = parser.parse_args()

    list_args.append(args.week)
    list_args.append(args.yoil)
    print(f"{list_args[0]}째주, {dict_yoil[list_args[1]]}요일")

    execute()