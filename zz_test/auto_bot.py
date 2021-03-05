import pyautogui as pg
import pyperclip
import time
import os
import numpy as np
import cv2
import threading

"""
# # 위치이동
# pg.moveTo(897, 455)
# # 클립보드에 복사
# pyperclip.copy("안녕하세요")
# # 해당 위치 클릭
# pg.click()
# # 클립보드 붙여넣기
# pg.hotkey('ctrl', 'v')
# # 엔터 입력
# pg.press('enter')

while True:
    print(pg.position())
    time.sleep(1)
"""

# capture = pg.screenshot('./images/saved_1.png')
# capture = cv2.cvtColor(np.array(capture), cv2.COLOR_RGB2BGR)
# cv2.imshow("image",capture)
# cv2.waitKey(1)


# im = pg.screenshot(region=(850, 300, 1600, 400))
# im = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
# cv2.imshow("image", im)
# print(pg.KEYBOARD_KEYS)
pg.press("prtsc")

def run_pgm():
    #os.system('""C:\\\\Program Files\\\\Notepad++\\\\notepad++.exe" -params "')
    os.system("C:/Windows/system32/mspaint.exe")


#pyperclip.copy("안녕하세요")
#os.system("C:/Windows/system32/mspaint.exe")
t = threading.Thread(target=run_pgm)
t.start()

#cv2.waitKey(1)
time.sleep(1)
#os.system(temp_var)
pg.moveTo(850, 300)
pg.click()
pg.hotkey('ctrl', 'v')

# 오른쪽 화면으로 이동
pg.moveTo(1556, 897)
pg.click()
pg.click()

# 선택 클릭
pg.moveTo(255, 126)
pg.click()

# 캡쳐 영역 선택하기
pg.moveTo(850, 300)
pg.dragTo(1400, 500, duration=1, button='left')
pg.mouseUp(1400, 500, button='left')

# 잘라내기
pg.hotkey('ctrl', 'x')
# 새 그림
pg.hotkey('ctrl', 'n')
# 잘라낸 부분 붙여넣기
pg.moveTo(871, 503)
pg.click()
pg.hotkey('ctrl', 'v')

#pyperclip.paste()
