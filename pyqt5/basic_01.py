## Ex 3-1. 창 띄우기.

import sys
# 필요한 모듈들을 불러옵니다. 기본적인 UI 구성요소를 제공하는 위젯 (클래스)들은 PyQt5.QtWidgets 모듈에 포함되어 있습니다.
from PyQt5.QtWidgets import QApplication, QWidget


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    # self는 MyApp 객체를 의미
    def initUI(self):
        # 창의 제목
        self.setWindowTitle('My First Application')
        # 위젯을 스크린의 x=300px, y=300px 위치로 이동
        self.move(300, 300)
        # 사이지를 너비 400px, 높이 300px 크기로 조절
        self.resize(400, 200)
        # 위젯을 스크린에 보여줌
        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())