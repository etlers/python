"""
    임진각 평화누리 캠핑장 예약
        - 렌탈B존 좌측 상단 2개
"""
from selenium import webdriver
import time, datetime

selenium_dir = "../../chromedriver/"
driver = webdriver.Chrome(selenium_dir + "chromedriver.exe")
url = 'http://imjingakcamping.co.kr/resv/res_01.html'
driver.get(url)

# 값 정의
# 6월 5일. # 마지막이 일자 열위치. 이전이 행위치            
resv_date = "/html/body/div[4]/div[1]/div/div[3]/div[2]/div[3]/span[7]/a"

###########################################################################################################################
# 사이트가 늦을 수 있어 해당 요소가 있는지 체크 적용
###########################################################################################################################
def execute():
    select_count = 0
    # 팝업 확인. 없을 수도 있음
    try:
        driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/form/div/span/a').click()
    except:
        time.sleep(0.1)
    # 6월로 선택
    str_ym = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[3]/div[1]/span').text
    if str_ym != "2021년 06월":
        while True:
            try:
                driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[3]/div[1]/a[2]/span").click()
                break
            except:
                time.sleep(0.1)
    # 날짜 선택
    while True:
        try:
            driver.find_element_by_xpath(resv_date).click()
            break
        except:
            time.sleep(0.1)
    # 유의사항 체크
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[7]/label").click()
            break
        except:
            time.sleep(0.1)
     
    # A존부터 시작해서 B존까지 인접 두개를 찾아서 선택
    def select_position(zone):
        result_tf = True
        # pos: 5,6,7,8
        # pos: 4,3,2,1
        # [3,4], [1,2], [1,8], [4,5], [5,6], [7,8], [2,3], [6,7], [3,6], [2,7]
        # /html/body/div[4]/div[1]/div/div[8]/div[7]/div[pos]/label
        list_pos = [
            [4,5], [3,4], [1,2], [1,8], [5,6], [7,8], [2,3], [6,7], [3,6], [2,7]
        ]
        # 체크박스가 있어야지 됨
        def check_checkbox(chk_pos_1, chk_pos_2):
            pos_tf = True
            try:                
                driver.find_element_by_xpath(chk_pos_1)
            except:
                pos_tf = False
            try:
                driver.find_element_by_xpath(chk_pos_2)
            except:
                pos_tf = False
            return pos_tf

        for pos in list_pos:
            if zone == 6:
                chk_pos_1 = '//*[@id="rc_a_' + str(pos[0]).zfill(2) + '"] '
                chk_pos_2 = '//*[@id="rc_a_' + str(pos[1]).zfill(2) + '"] '
            else:
                chk_pos_1 = '//*[@id="rc_' + str(pos[0]).zfill(2) + '"] '
                chk_pos_2 = '//*[@id="rc_' + str(pos[1]).zfill(2) + '"] '
            # 존재하는 경우
            if check_checkbox(chk_pos_1, chk_pos_2) == True:
                # A. /html/body/div[4]/div[1]/div/div[8]/div[7]/div[7]/label
                # B. /html/body/div[4]/div[1]/div/div[8]/div[8]/div[7]/label
                if zone == 6:
                    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[8]/div[7]/div[' + str(pos[0]) + ']/label').click()
                    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[8]/div[7]/div[' + str(pos[1]) + ']/label').click()
                    result_tf = True
                else:
                    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[8]/div[8]/div[' + str(pos[0]) + ']/label').click()
                    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[8]/div[8]/div[' + str(pos[1]) + ']/label').click()
                    result_tf = True
            else:
                result_tf = False
            if result_tf == True: break
        return result_tf

    # 렌탈캠핑존. button[6 or 7]. 6-A, 7-B
    def click_zone(str_zone):
        while True:
            try:
                driver.find_element_by_xpath(str_zone)
                break                
            except:
                time.sleep(0.1)
        driver.find_element_by_xpath(str_zone).click()

    list_zone = [6, 7]
    for zone in list_zone:
        str_zone = "/html/body/div[4]/div[1]/div/div[8]/div[1]/button[" + str(zone) + "]"
        click_zone(str_zone)
        # 사이트 체크하는 화면이 떴는지 확인
        while True:
            try:
                driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[8]/div[7]/div[1]")
                break
            except:
                time.sleep(0.1)
        # 사이트 체크
        pos_tf = select_position(zone)
        if pos_tf == True:
            select_count = 2
            break
    # 남은 자리가 없었다면...
    if select_count == 0:
        print("No Position")
        return 1
    
    driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[8]/div[1]/button[7]").click()
    # 위치 선택
    while True:
        try:
            driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[8]/div[8]/div[5]/label').click()
            break
        except:
            time.sleep(0.1)
    while True:
        try:
            driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[8]/div[8]/div[6]/label').click()
            break
        except:
            time.sleep(0.1)
    # 인원수 선택
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[9]/form/div[1]/div[1]/table/tbody/tr[1]/td[4]/select/option[3]").click()
            break
        except:
            time.sleep(0.1)
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[9]/form/div[1]/div[2]/table/tbody/tr[1]/td[4]/select/option[3]").click()
            break
        except:
            time.sleep(0.1)
    # 예약하기
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[9]/div[2]/button").click()
            break
        except:
            time.sleep(0.1)

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

    # 예약정보
    send_resv_info("/html/body/div[4]/div[5]/div/form/fieldset/div/dl[1]/dd[1]/input", "최주용")
    send_resv_info("/html/body/div[4]/div[5]/div/form/fieldset/div/dl[1]/dd[2]/input", "010-5000-6104")
    send_resv_info("/html/body/div[4]/div[5]/div/form/fieldset/div/dl[2]/dd/input", "cazoobong@naver.com")
    send_resv_info("/html/body/div[4]/div[5]/div/form/fieldset/div/dl[3]/dd/input", "721005")
    send_resv_info("/html/body/div[4]/div[5]/div/form/fieldset/div/dl[4]/dd/input", "22노3140")
    # 약관
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[5]/div/form/div[13]/label").click()
            break
        except:
            time.sleep(0.1)
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[5]/div/form/div[15]/label").click()
            break
        except:
            time.sleep(0.1)
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[5]/div/form/div[16]/label").click()
            break
        except:
            time.sleep(0.1)
    # 예약하기
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[5]/div/form/div[17]/button").click()            
            break
        except:
            time.sleep(0.1)
    """
    # 결재 팝업
    # /html/body/div[3]/form/div[2]/div[2]/div[1]/div[2]/div[1]/label
    # /html/body/div[3]/form/div[2]/div[2]/div[1]/div[2]/div[1]/label/span
    # /html/body/div[3]/form/div[2]/div[2]/div[1]/div[2]/div[1]/label/span/img
    # 전체동의. 
    while True:
        try:
            driver.find_element_by_xpath('/html/body/div[3]/form/div[2]/div[2]/div[1]/div[2]/div[1]/label/span').click()
            break
        except:
            time.sleep(0.1)
    # 현대카드 선택. 
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[3]/form/div[2]/div[2]/div[3]/div/div/span[2]/a/span/span[2]").click()
            break
        except:
            time.sleep(0.1)
    # 무이자선택. 
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[3]/form/div[2]/div[2]/div[5]/select/option[2]").click()
            break
        except:
            time.sleep(0.1)
    # 현대앱카드 결재. 
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[3]/form/div[2]/div[2]/div[5]/div[1]/label/span[1]").click()
            break
        except:
            time.sleep(0.1)
    """

if __name__ == "__main__":
    # 10시 이전까지는 확인
    while True:
        # 시간 체크
        now = datetime.datetime.now() # current date and time
        run_hms = now.strftime("%H%M%S")
        # 10시가 되면 시작하고 종료
        if run_hms > "095956":
            execute()
            break
        # 대기
        print(run_hms)
        time.sleep(0.5)