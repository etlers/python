"""
    임진각 평화누리 캠핑장 카라반 빈자리 찾아서 예약하기
    화면을 띄운 후 다음 월로 변경을 하고 기다리면 10시에 시작을 함
"""
from selenium import webdriver
import time, datetime, yaml
import argparse
import random

selenium_dir = "../chromedriver/"
driver = webdriver.Chrome(selenium_dir + "chromedriver.exe")
url = 'http://imjingakcamping.co.kr/resv/res_01.html'
driver.get(url)

# 프로그램 메세지
pgm_msg = """
# 임진각 평화누리 캠핑장 카라반 빈자리 찾아서 예약하기
# 화면을 띄운 후 다음 월로 변경을 하고 기다리면 10시에 시작을 함
"""
print(pgm_msg)

# 토요일 행 위치 지정. 2-7, 3-7, 4-7, 5-7, 6-7
day_col_num = 4
list_day_num_ir = [5, 4, 6, 3, 2]
# 존에 대한 번호. xpath 배열 번호에 사용됨
dict_zone_info = {
    "A": ["8", 14],
    "B": ["9", 15],
    "C": ["10", 9],
}
# 존 자리 위치
list_nums = []

with open('./config.yaml', encoding="utf-8") as stream:
    try:
        dict_config = yaml.safe_load(stream)
        resv_ym = dict_config['resv_ym']
    except yaml.YAMLError as exc:
        print(exc)

# 받은 경로로 존(카라반존A, B, C) 클릭
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
    for pos in list_nums:
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

    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[9]/form/div[1]/div/table/tbody/tr[1]/td[4]/select/option[5]").click()
            print("사이트 선택")
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

    # 날짜가 제대로 선택이 됐는지 확인. 선택이 안되면 우측 일자와 다름
    def check_date_selected(calendar_day):
        # 우측에 보이는 날짜
        view_month = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[4]/div/strong[2]').text
        view_day = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[4]/div/strong[3]').text
        # 입력받은 날짜
        in_month = resv_ym.split(" ")[1].replace("월","")
        month_day = in_month + calendar_day.zfill(2)
        print(month_day, view_month + view_day)
        # 일치여부 확인
        if month_day == view_month + view_day:
            return True
        else:
            return False
    
    rsvym_tf = True
    # 지정한 월로 변경될 때까지 대기
    while rsvym_tf:
        # 화면에서 달력의 년월 추출
        site_ym = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[3]/div[1]/span').text
        if site_ym == resv_ym:
            # 달력이 선택 되었다는 의미
            rsvym_tf = False
            # 예약하기 버튼이 생성됐는지 확인. 있다면 화면이 떴다는 의미
            while True:
                try:
                    rsv_btn = driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[9]/div[2]/button").text
                    time.sleep(0.1)
                    break
                except:
                    time.sleep(0.5)                
            # 지정한 일자 순서에 따라 확인
            for ir in list_day_num_ir:                
                # 달력의 일자 가져오기
                try:
                    calendar_day = driver.find_element_by_xpath(f"/html/body/div[4]/div[1]/div/div[3]/div[2]/div[{ir}]/span[{day_col_num}]/a").text
                except:
                    calendar_day = ""                
                # 공백으로 일자가 아닌 경우
                if len(calendar_day) == 0:
                    print(f"{ir}번째는 일자가 아닙니다.")
                    continue
                # 달력 일자 선택
                try:
                    driver.find_element_by_xpath(f"/html/body/div[4]/div[1]/div/div[3]/div[2]/div[{ir}]/span[{day_col_num}]/a").click()
                except:
                    # 회색의 경우 클릭이 안됨
                    print(f"{calendar_day}일은 선택할 수 없는 일자입니다.")
                    continue
                # 달력 선택여부
                # selected_tf = check_date_selected(calendar_day)
                # 제대로 일자 선택이 됐다면
                # 사이트 빈자리 추출
                empty_cnt_a, empty_cnt_b, empty_cnt_c = site_count()
                # 존에 빈자리가 있었다면
                if ((zone_cd == "A" and empty_cnt_a > 0) or (zone_cd == "B" and empty_cnt_b > 0) or (zone_cd == "C" and empty_cnt_c > 0)):
                    break
                else:
                    print(f"존 {zone_cd}에 빈자리가 자리가 없습니다.")
        else:
            time.sleep(0.5)
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


# 최초 팝업을 클릭해서 없애서 예약을 위한 사이트 체크로 들어감
def execute(zone_cd):
    # 팝업 확인. 없을 수도 있음
    try:
        driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/form/div/span/a').click()
    except:
        time.sleep(0.1)
    # 예약 사전 준비 및 사이트 확인
    if prepare_for_reservation(zone_cd):
        reservation_click()
        pass
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
            if num not in list_nums:
                list_nums.append(num)    
            if len(list_nums) == position_cnt: break

    # 프로그램에서 예약할 사이트 인자 받아오기
    parser = argparse.ArgumentParser(description='Karaban Site Argument. A, B, C')
    parser.add_argument('--zone', help='A, B, C')
    args = parser.parse_args()
    print("Karaban Zone: ", args.zone.upper())
    
    make_zone_position_num(args.zone.upper())
    
    # 10시 이전까지는 확인
    while True:
        # 시간 체크
        now = datetime.datetime.now()
        run_hms = now.strftime("%H%M%S")
        # 10시가 되면 시작하고 종료
        if run_hms >= "134001":
            break
        else:
            # 대기
            print(run_hms)
            time.sleep(0.5)
    # 실제 작업 시작
    execute(args.zone.upper())