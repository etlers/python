## Ex 3-7. 툴바 만들기 & 창을 화면 중앙으로

"""
한 개의 메뉴를 갖는 툴바를 만들었습니다.
툴바에는 선택되었을 때 어플리케이션을 종료하는 'exitAction'이 하나 포함되어 있습니다.
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QWidget, QDesktopWidget
from PyQt5.QtGui import QIcon


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 메뉴바의 경우와 마찬가지로 QAction 객체를 하나 생성합니다.
        # 이 객체는 아이콘 (exit.png), 라벨 ('Exit')을 포함하고, 단축키 (Ctrl+Q)를 통해 실행 가능합니다.
        # 상태바에 메세지 ('Exit application')를 보여주고, 클릭 시 생성되는 시그널은 quit() 메서드에 연결되어 있습니다.
        exitAction = QAction(QIcon('./img/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        # addToolbar()를 이용해서 툴바를 만들고, addAction()을 이용해서 툴바에 exitAction 동작을 추가했습니다.
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        self.setWindowTitle('Toolbar & Centering')
        #self.setGeometry(500, 350, 300, 200)
        self.resize(500, 350)
        self.center()
        self.show()

    # 중앙으로 위치
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())