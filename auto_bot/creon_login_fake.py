import pyautogui
import time

position = pyautogui.position()

def key_press(char):
    pyautogui.press(char)
    # pyautogui.keyUp(char)

# 실행
pyautogui.moveTo(37, 729, 1)
pyautogui.doubleClick()
time.sleep(7)
# 모의투자
pyautogui.moveTo(978, 647, 1)
pyautogui.click()
time.sleep(1)
#
pyautogui.moveTo(957, 492, 1)
pyautogui.click()
time.sleep(1)
# 비번
pyautogui.moveTo(1169, 432, 0.1)
pyautogui.click()
pyautogui.moveTo(1235, 389, 0.1)
pyautogui.click()
pyautogui.moveTo(1256, 389, 0.1)
pyautogui.click()
pyautogui.moveTo(1257, 493, 0.1)
pyautogui.click()
pyautogui.moveTo(1257, 472, 0.1)
pyautogui.click()
pyautogui.moveTo(1192, 472, 0.1)
pyautogui.click()
pyautogui.moveTo(1192, 492, 0.1)
pyautogui.click()
time.sleep(1)
# 로그인
pyautogui.moveTo(974, 604, 1)
pyautogui.click()
time.sleep(30)
# 참여 모의투자 선택
pyautogui.moveTo(975, 575, 1)
time.sleep(1)
pyautogui.click()