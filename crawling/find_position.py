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

resv_ym = "2021년 06월"
list_yoil = [6, 7]

# with open('./config.yaml', encoding="utf-8") as stream:
#     try:
#         dict_config = yaml.safe_load(stream)
#         resv_ym = dict_config['resv_ym']
#     except yaml.YAMLError as exc:
#         print(exc)


def reservation():
    pass

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

    list_weeks = [2, 3, 4, 5, 6, 7]
    for week in list_weeks:
        for yoil in list_yoil:
            try:
                resv_path = f'/html/body/div[4]/div[1]/div/div[3]/div[2]/div[{week}]/span[{yoil}]/a'
                calendar_day = driver.find_element_by_xpath(resv_path).text
            except:
                calendar_day = ""
            # 공백으로 일자가 아닌 경우
            if len(calendar_day) == 0:
                print(f"{week}번째는 일자가 아닙니다.")
                continue
            print(calendar_day, week, yoil)

            driver.find_element_by_xpath(resv_path).click()
            
            rental_a_cnt = int(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[4]/table/tbody/tr/td[5]/span').text)
            # if rental_a_cnt > 0:
            #     end_tf = reservation(resv_path, "6")
            #     if end_tf: break
            rental_b_cnt = int(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[4]/table/tbody/tr/td[6]/span').text)
            # if rental_b_cnt > 0:
            #     end_tf = reservation(resv_path, "7")
            #     if end_tf: break
            print(target_day, rental_a_cnt, rental_b_cnt)

        # if end_tf: break
            

if __name__ == "__main__":
    execute()
    # driver.close()