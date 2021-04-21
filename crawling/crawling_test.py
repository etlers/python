from selenium import webdriver

selenium_dir = "../../chromedriver/"

driver = webdriver.Chrome(selenium_dir + "chromedriver.exe")
url='https://www.naver.com/' # 접속하고자 하는 웹사이트 주소
driver.get(url) # driver 객체에 해당 url의 응답을 받아오라는 명령 -> 이 사이트로 접속해라

find = driver.find_element_by_xpath("//input[@id='query']")
find.clear()  # 글자 지움
find.send_keys("SRT 취소표") # 글자 입력

search = driver.find_element_by_xpath("//button[@type='submit']") # 검색(돋보기) 버튼 요소
search.click() # 요소 클릭

driver.switch_to.window(driver.window_handles[-1]) # 최신 팝업창으로 이동
driver.switch_to.window(driver.window_handles[0]) # 원래 창으로 복귀

driver.close() # 크롬 끄기