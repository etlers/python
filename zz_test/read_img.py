import cv2
import pytesseract
from  PIL import Image
import time

"""
fname = './images/nums.png'

original = cv2.imread(fname, cv2.IMREAD_COLOR)
gray = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
unchange = cv2.imread(fname, cv2.IMREAD_UNCHANGED)

cv2.imshow('Original', original)
cv2.imshow('Gray', gray)
cv2.imshow('Unchange', unchange)

cv2.waitKey(1)
cv2.destroyAllWindows()

cv2.imwrite('./images/original.png', original)
cv2.imwrite('./images/gray.png', gray)

#pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
nums = pytesseract.image_to_string(Image.open('./images/gray.png'), lang='kor')
# value = Image.open("./images/gray.png")
# nums = pytesseract.image_to_string(value, config='')
print(nums)

img_cv = cv2.imread(r'./images/gray.png')

# By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
# we need to convert from BGR to RGB format/mode:
img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
print(pytesseract.image_to_string(img_rgb))
# OR
img_rgb = Image.frombytes('RGB', img_cv.shape[:2], img_cv, 'raw', 'BGR', 0, 0)
print(pytesseract.image_to_string(img_rgb))

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
#nums = pytesseract.image_to_string(Image.open('./images/gray.png'), lang='kor')
value = Image.open("./images/nums.png")
nums = pytesseract.image_to_string(value, config='')
print(nums)
"""
# 850, 300 - 1600, 400
# 캡쳐 영역 선택하기
pg.moveTo(850, 300)
pg.dragTo(1600, 400, duration=1, button='left')
time.sleep(1)
pg.mouseUp(1600, 400, button='left')
time.sleep(1)

