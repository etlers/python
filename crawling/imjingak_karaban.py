"""
    임진각 평화누리 캠핑장 예약
        - 빈자리 찾아서 예약하기 - 카라반
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


def reservation(zone_cd):
    result_tf = False
    # 유의사항 체크
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[7]/label").click()
            result_tf = True
            break
        except:
            time.sleep(0.1)

    # 카라반존. zone_cd = 8, 9, 10
    def click_zone(zone_path):
        while True:
            try:
                tmp = driver.find_element_by_xpath(zone_path).text
                break                
            except:
                time.sleep(0.1)
        driver.find_element_by_xpath(zone_path).click()

    zone_path = f"/html/body/div[4]/div[1]/div/div[8]/div[1]/button[{zone_cd}]"
    click_zone(zone_path)
    
    # 사이트 체크하는 화면이 떴는지 확인
    while True:
        try:
            driver.find_element_by_xpath(f"/html/body/div[4]/div[1]/div/div[8]/div[{(int(zone_cd)+1)}]")
            result_tf = True
            break
        except:
            time.sleep(0.1)
    
    # 체크박스가 있어야지 됨
    def review_checkbox(chk_position):
        position_tf = True
        try:
            tmp = driver.find_element_by_xpath(chk_position).text
            print(chk_position, tmp, len(tmp))
        except:
            position_tf = False

        return position_tf

    dict_position = {
        "8": ["cv_a", 14],
        "9": ["cv_b", 15],
        "10": ["cv_c", 9],
    }
    
    for num in range(dict_position[zone_cd][1]):
        pos = str(num + 1).zfill(2)
        chk_position = f'//*[@id="{dict_position[zone_cd][0]}_{pos}"]'
        if review_checkbox(chk_position) == True:
            driver.find_element_by_xpath(f'/html/body/div[4]/div[1]/div/div[8]/div[{str(int(zone_cd)+1)}]/div[{num}]/label').click()
            result_tf = True
            break

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
    end_tf = False
    # 날짜
    for ir in range(6):
        for ic in range(7):
            try:
                resv_path = f'/html/body/div[4]/div[1]/div/div[3]/div[2]/div[{ir+1}]/span[{ic+1}]/a'
                try:
                    target_day = int(driver.find_element_by_xpath(resv_path).text)
                except:
                    target_day = 0
                if target_day == 0: continue
                
                driver.find_element_by_xpath(f'/html/body/div[4]/div[1]/div/div[3]/div[2]/div[{ir+1}]/span[{ic+1}]/a').click()
                time.sleep(0.5)
                empty_cnt_a = int(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[4]/table/tbody/tr/td[7]/span').text)
                empty_cnt_b = int(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[4]/table/tbody/tr/td[8]/span').text)
                empty_cnt_c = int(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[4]/table/tbody/tr/td[9]/span').text)
                # print(empty_cnt_a, empty_cnt_b, empty_cnt_c)
                if empty_cnt_a > 0:
                    end_tf = reservation("8")
                    if end_tf: return True
                if empty_cnt_b > 0:
                    end_tf = reservation("9")
                    if end_tf: return True
                if empty_cnt_c > 0:
                    end_tf = reservation("10")
                    if end_tf: return True
            except:
                pass            
        if end_tf: return True
            

if __name__ == "__main__":
    if execute() == True:
        print("True")
    else:
        driver.close()