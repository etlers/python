from selenium import webdriver
import time, datetime, requests
from bs4 import BeautifulSoup as bs

selenium_dir = "../../chromedriver/"
driver = webdriver.Chrome(selenium_dir + "chromedriver.exe")
url = 'http://imjingakcamping.co.kr/resv/res_01.html'
driver.get(url)

try:
    driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[3]/div[2]/div[6]/span[5]/a")
    print("True")
except:
    print("False")