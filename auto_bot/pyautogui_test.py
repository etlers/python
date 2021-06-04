import pyautogui as pg
import time
import pyperclip

"""
# 좌표 객체 얻기 
position = pg.position()
# 화면 전체 크기 확인하기
print(pg.size())
# x, y 좌표
print(position.x)
print(position.y)
# 마우스 이동 (x 좌표, y 좌표)
pg.moveTo(500, 500)
# 마우스 이동 (x 좌표, y 좌표 2초간)
pg.moveTo(100, 100, 2)  
# 마우스 이동 ( 현재위치에서 )
pg.moveRel(200, 300, 2)
# 마우스 클릭
pg.click()
# 2초 간격으로 2번 클릭
pg.click(clicks= 2, interval=2)
# 더블 클릭
pg.doubleClick()
# 오른쪽 클릭
pg.click(button='right')
# 스크롤하기 
pg.scroll(10)
# 드래그하기
pg.drag(0, 300, 1, button='left')
#542, 555
while True:
    print(pg.position())
    time.sleep(1)
# 마우스 이동 (x 좌표, y 좌표)
pg.moveTo(468, 287)
pg.click()
time.sleep(1)
pyperclip.copy('mac')

pg.hotkey("ctrl", "v")
#pg.typewrite("galaxy")
pg.press("enter")

while True:
    pg.moveTo(1250, 300)
    time.sleep(1)
    pg.moveTo(1270, 200)
    time.sleep(1)
    pg.moveTo(1170, 250)
    time.sleep(1)
"""
pg.moveTo(2287, 1424)
time.sleep(1)
pg.click()
time.sleep(1)
pg.moveTo(2572, 82)
time.sleep(1)
pg.click()
time.sleep(1)
pg.write("https://etlers.slack.com/apps/A0F7XDUAZ-incoming-webhooks")

pg.write("\n")