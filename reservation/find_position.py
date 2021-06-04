"""
    임진각 평화누리 캠핑장 예약
        - 지정한 일자의 빈자리 찾아서 예약하기
"""
from selenium import webdriver
import time, datetime, yaml

selenium_dir = "../chromedriver/"
driver = webdriver.Chrome(selenium_dir + "chromedriver.exe")
url = 'http://imjingakcamping.co.kr/resv/res_01.html'
driver.get(url)


def reservation():
    pass

def execute():

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

    def check_day_avali(resv_path):        
        driver.find_element_by_xpath(resv_path).click()        
        # 제대로 일자 선택이 됐다면 사이트 빈자리 추출
        empty_cnt_a, empty_cnt_b, empty_cnt_c = site_count()
        print(empty_cnt_a, empty_cnt_b, empty_cnt_c)
    
    # 팝업 확인. 없을 수도 있음
    try:
        driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/form/div/span/a').click()
    except:
        time.sleep(0.1)

    list_weeks = [2, 3, 4, 5, 6, 7]
    list_yoil = [6, 7]

    for week in list_weeks:
        for yoil in list_yoil:
            try:
                resv_path = f'/html/body/div[4]/div[1]/div/div[3]/div[2]/div[{week}]/span[{yoil}]/a'
                calendar_day = driver.find_element_by_xpath(resv_path).text
                print(calendar_day, week, yoil)        
                check_day_avali(resv_path)                
            except:
                print(f"[{week}, {yoil}] 위치는 일자가 아닙니다.")
                continue
            

if __name__ == "__main__":
    execute()
    # driver.close()