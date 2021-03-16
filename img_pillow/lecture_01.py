# 이미지 돌리기
from PIL import Image
import glob, os
"""
im = Image.open("./img/whatu.png")
im.rotate(180).show()
"""
size = 128, 128

for infile in glob.glob("./img/*.png"):
    file, ext = os.path.splitext(infile)
    im = Image.open(infile)
    im = im.convert("RGB")
    im.thumbnail(size)
    im.save(file + ".thumbnail", "JPEG")