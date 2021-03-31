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
      # 푸시버튼 생성. 이 버튼 (btn)은 QPushButton 클래스의 인스턴스
      # 생성자 (QPushButton())의 첫 번째 파라미터에는 버튼에 표시될 텍스트를 두 번째 파라미터에는 버튼이 위치할 부모 위젯을 입력
      btn = QPushButton('Quit', self)
      btn.move(50, 50)
      btn.resize(btn.sizeHint())
      # PyQt5에서의 이벤트 처리는 시그널과 슬롯 메커니즘으로 이루어집니다.
      # 버튼 (btn)을 클릭하면 'clicked' 시그널이 만들어집니다.
      # instance() 메서드는 현재 인스턴스를 반환합니다.
      # 'clicked' 시그널은 어플리케이션을 종료하는 quit() 메서드에 연결됩니다.
      # 이렇게 발신자 (Sender)와 수신자 (Receiver), 두 객체 간에 커뮤니케이션이 이루어집니다.
      # 이 예제에서 발신자는 푸시버튼 (btn)이고, 수신자는 어플리케이션 객체 (app)입니
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