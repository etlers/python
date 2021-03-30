## Ex 3-2. 어플리케이션 아이콘 넣기 및 창 닫기.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication


class MyApp(QWidget):

  def __init__(self):
      super().__init__()
      self.initUI()

  def initUI(self):

      btn = QPushButton('Quit', self)
      btn.move(50, 50)
      btn.resize(btn.sizeHint())
      btn.clicked.connect(QCoreApplication.instance().quit)

      self.setWindowTitle('etlers')
      # 어플리케이션 아이콘을 설정
      self.setWindowIcon(QIcon('./img/etlers.png'))
      # 창의 위치와 크기를 설정
      # 앞의 두 매개변수는 창의 x, y 위치를 결정하고, 뒤의 두 매개변수는 각각 창의 너비와 높이를 결정
      # move()와 resize() 메서드를 하나로 합쳐놓은 것과 동일
      self.setGeometry(300, 300, 300, 200)
      self.show()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = MyApp()
  sys.exit(app.exec_())