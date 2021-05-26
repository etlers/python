from selenium import webdriver
import time, datetime, requests
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

selenium_dir = "../../chromedriver/"
driver = webdriver.Chrome(selenium_dir + "chromedriver.exe")
url = 'http://imjingakcamping.co.kr/resv/res_01.html'
driver.get(url)

# 팝업 확인. 없을 수도 있음
try:
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/form/div/span/a').click()
except:
    time.sleep(0.1)

driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[8]/div[1]/button[7]').click()
time.sleep(1)

try:
    #driver.find_element_by_id("rc_06").click()
    val = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[3]/div[1]/span').text
    print(val)
    # driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[3]/div[1]/a[2]/span').click()
    # elem = driver.find_element_by_xpath("//span[text()='다음달']")
    # driver.find_element_by_xpath('//*[@id="contents"]/div/div[3]/div[1]/a[2]/span').click()
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='다음달']"))).click()
    while True:
        try:
            print(driver.find_element_by_xpath('//*[@id="contents"]/div/div[3]/div[1]/a[2]/span').text)
            driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[3]/div[1]/a[2]/span").click()
            break
        except:
            time.sleep(1)
    # elem.click()
    # elem.click()
    
except:
    print("False")