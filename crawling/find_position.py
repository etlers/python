"""
    임진각 평화누리 캠핑장 예약
        - 빈자리 찾아서 예약하기
"""
from selenium import webdriver
import time, datetime, yaml

selenium_dir = "../../chromedriver/"
driver = webdriver.Chrome(selenium_dir + "chromedriver.exe")
url = 'http://imjingakcamping.co.kr/resv/res_01.html'
driver.get(url)

# 6월 5일. # 마지막이 일자 열위치. 이전이 행위치. row: 1~6, col: 1~7
resv_date = "/html/body/div[4]/div[1]/div/div[3]/div[2]/div[2]/span[7]/a"

with open('./config.yaml', encoding="utf-8") as stream:
    try:
        dict_config = yaml.safe_load(stream)
        resv_ym = dict_config['resv_ym']
    except yaml.YAMLError as exc:
        print(exc)


def reservation(resv_path, zone_cd):
    result_tf = False
    # 날짜 선택
    while True:
        try:
            driver.find_element_by_xpath(resv_path).click()
            break
        except:
            time.sleep(0.1)
    # 유의사항 체크
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[7]/label").click()
            result_tf = True
            break
        except:
            time.sleep(0.1)

    # 렌탈캠핑존. button[6 or 7]. 6-A, 7-B
    def click_zone(zone_path):
        while True:
            try:
                driver.find_element_by_xpath(zone_path)
                break                
            except:
                time.sleep(0.1)
        driver.find_element_by_xpath(zone_path).click()

    zone_path = f"/html/body/div[4]/div[1]/div/div[8]/div[1]/button[{zone_cd}]"
    click_zone(zone_path)
    # 사이트 체크하는 화면이 떴는지 확인
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[8]/div[7]/div[1]")
            result_tf = True
            break
        except:
            time.sleep(0.1)

    # 체크박스가 있어야지 됨
    def review_checkbox(chk_position):
        position_tf = True
        try:                
            driver.find_element_by_xpath(chk_position)
        except:
            position_tf = False

    dict_position = {
        "6": "rc_a_",
        "7": "rc_",
    }
    list_pos = [
        "04", "05", "08", "06", "07", "01", "03", "02"
    ]
    for pos in list_pos:
        chk_position = f'//*[@id="{dict_position[zone_cd]}_{pos}"]'
        if review_checkbox(chk_position) == True:
            driver.find_element_by_xpath(f'/html/body/div[4]/div[1]/div/div[8]/div[{str(int(zone_cd)+1)}]/div[{pos}]/label').click()

    return result_tf


def execute():
    
    select_count = 0
    # 팝업 확인. 없을 수도 있음
    try:
        driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/form/div/span/a').click()
    except:
        time.sleep(0.1)
    # 6월로 선택
    site_ym = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[3]/div[1]/span').text
    if site_ym != resv_ym:
        while True:
            try:
                driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[3]/div[1]/a[2]/span").click()
                break
            except:
                time.sleep(0.1)
    # 날짜 선택
    # while True:
    #     try:
    #         driver.find_element_by_xpath(resv_date).click()
    #         break
    #     except:
    #         time.sleep(0.1)
    end_tf = False
    for ir in range(6):
        for ic in range(7):
            try:
                resv_path = f'/html/body/div[4]/div[1]/div/div[3]/div[2]/div[{ir+1}]/span[{ic+1}]/a'
                target_day = int(driver.find_element_by_xpath(resv_path).text)
                driver.find_element_by_xpath(f'/html/body/div[4]/div[1]/div/div[3]/div[2]/div[{ir+1}]/span[{ic+1}]/a').click()
                time.sleep(0.5)
                rental_a_cnt = int(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[4]/table/tbody/tr/td[5]/span').text)
                if rental_a_cnt > 0:
                    end_tf = reservation(resv_path, "6")
                    if end_tf: break
                rental_b_cnt = int(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[4]/table/tbody/tr/td[6]/span').text)
                if rental_b_cnt > 0:
                    end_tf = reservation(resv_path, "7")
                    if end_tf: break
            except:
                pass            
        if end_tf: break
            

if __name__ == "__main__":
    execute()
    # driver.close()