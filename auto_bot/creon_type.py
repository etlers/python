from pywinauto.application import Application
import pywinauto.mouse as mouse
import pywinauto.keyboard as keyboard

app = Application().start(r"C:\CREON\STARTER\coStarter.exe")

app = Application().connect(path=r"C:\CREON\STARTER\coStarter.exe")
app.dlg.control #first method
app['dlg']['control'] #second method is preferred as it is more robust for unicode strings
app.windows()

# dlg = app['제목 없음 - Windows 메모장Notepad']

# # dlg.print_control_identifiers()

# dlg.set_focus()
keyboard.send_keys('Hello')