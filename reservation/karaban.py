"""
    임진각 평화누리 캠핑장 카라반 빈자리 찾아서 예약하기
    화면을 띄운 후 다음 월로 변경을 하고 기다리면 10시에 시작을 함
"""
from selenium import webdriver
import time, datetime
import argparse
import random

selenium_dir = "../chromedriver/"
driver = webdriver.Chrome(selenium_dir + "chromedriver.exe")
url = 'http://imjingakcamping.co.kr/resv/res_01.html'
driver.get(url)

# 프로그램 메세지
pgm_msg = """
# 임진각 평화누리 캠핑장 카라반 지정한 일자에 빈자리 찾아서 예약하기
# 화면을 띄운 후 다음 월로 변경을 하고 기다리면 10시에 시작을 함
"""
print(pgm_msg)
# 입력인자 저장
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
# 존 자리 위치
list_zone_position = []

# 받은 경로로 존(카라반존 A, B, C) 클릭
def click_zone(zone_path):
    # 존 명칭이 나올 때까지 대기
    while True:
        try:
            zone_nm = driver.find_element_by_xpath(zone_path).text
            print(zone_nm)
            break                
        except:
            time.sleep(0.1)
    # 존 클릭
    driver.find_element_by_xpath(zone_path).click()

# 존 번호를 받아서 빈자리 확인하고 선택까지 함
def click_empty_site(zone_cd):
    # 자리 클릭을 못한 경우
    click_tf = False
    zone_num = dict_zone_info[zone_cd][0]
    # 전체 개수를 돌면서 빈자리가 있는지 확인
    for pos in list_zone_position:
        # 마감이 있으면 지나감
        try:
            magam = driver.find_element_by_xpath(f"/html/body/div[4]/div[1]/div/div[8]/div[{int(zone_num)+1}]/div[{pos}]/span").text
        except:
            magam = "NO"
        # 마감이 아닌 경우 클릭
        if magam == "NO":
            driver.find_element_by_xpath(f'/html/body/div[4]/div[1]/div/div[8]/div[{int(zone_num)+1}]/div[{pos}]/label').click()
            click_tf = True
            break

    return click_tf


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

# 예약 시작을 위한 사전 준비
def prepare_for_reservation(zone_cd):

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
    week_num = list_args[1] + 1
    day_col_num = list_args[2]
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
    # 존에 빈자리가 있었다면
    if ((zone_cd == "A" and empty_cnt_a == 0) or (zone_cd == "B" and empty_cnt_b == 0) or (zone_cd == "C" and empty_cnt_c == 0)):
        return False

    # 존에 맞는 빈자리를 찾지 못하고 나왔다면
    if ((zone_cd == "A" and empty_cnt_a == 0) or (zone_cd == "B" and empty_cnt_b == 0) or (zone_cd == "C" and empty_cnt_c == 0)):
        return False

    # 유의사항 체크
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[7]/label").click()
            break
        except:
            time.sleep(0.1)

    # Zone에 빈자리가 있으면 카라반 존 클릭하러 들어감
    zone_num = dict_zone_info[zone_cd][0]
    # xpath 경로를 주고 존 클릭하러 들어감
    click_zone(f'/html/body/div[4]/div[1]/div/div[8]/div[1]/button[{zone_num}]')
    # 존에 대한 사이트 확인 및 빈자리 선택
    if click_empty_site(zone_cd):
        return True
    else:
        return False


# 최초 팝업을 클릭해서 없애고 예약을 위한 사이트 체크로 들어감
def execute():
    # 팝업 확인. 없을 수도 있음
    try:
        driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/form/div/span/a').click()
    except:
        time.sleep(0.1)
    # 예약 사전 준비 및 사이트 확인
    if prepare_for_reservation(list_args[0]):
        reservation_click()
    else:
        print("예약 실패!!!")
        driver.close()
            

# 프로그램 시작
if __name__ == "__main__":

    # 존에 대한 자리 찾을 순서 임의로 구성
    def make_zone_position_num(zone_cd):
        position_cnt = dict_zone_info[zone_cd][1]
        # 존에 대한 리스트 생성
        while True:
            num = random.randint(1, position_cnt)
            if num not in list_zone_position:
                list_zone_position.append(num)    
            if len(list_zone_position) == position_cnt: break

    # 프로그램에서 예약할 사이트 인자 받아오기
    parser = argparse.ArgumentParser(description='Karaban Site Argument. A, B, C')
    parser.add_argument('--zone', help='A, B, C')
    parser.add_argument('--week', type=int, help='1 ~ 6')
    parser.add_argument('--yoil', type=int, help='Sun ... Sat: 1 ~ 7')
    args = parser.parse_args()

    list_args.append(args.zone.upper())
    list_args.append(args.week)
    list_args.append(args.yoil)
    print(f"카라반 존 {list_args[0]}  {list_args[1]}째주 {dict_yoil[list_args[2]]}요일")

    make_zone_position_num(list_args[0])
    
    # # 10시 이전까지는 확인
    # while True:
    #     # 시간 체크
    #     now = datetime.datetime.now()
    #     run_hms = now.strftime("%H%M%S")
    #     # 10시가 되면 시작하고 종료
    #     if run_hms > "100002":
    #         break
    #     else:
    #         # 대기
    #         print(run_hms)
    #         time.sleep(0.5)
    # 실제 작업 시작
    execute()