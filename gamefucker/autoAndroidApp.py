# -*- coding: utf-8 -*-
# [pywinauto简明教程](https://gaianote.github.io/2018/06/13/pywinauto%E7%AE%80%E6%98%8E%E6%95%99%E7%A8%8B/)
# [pywinauto UserGuide](https://pywinauto.readthedocs.io/en/latest/getting_started.html)
# [PyWinAuto入门指南](https://zhuanlan.zhihu.com/p/37283722)
# [在中文windows下使用pywinauto进行窗口操作（一）](https://my.oschina.net/yangyanxing/blog/167042)
import pyautogui
from pywinauto.application import Application

pyautogui.PAUSE = 1.5
pyautogui.FAILSAFE = True

__DEBUG__=True

if __name__ == "__main__":
    # get the size of the screen
    if __DEBUG__ == True:
        print "screen size:", pyautogui.size()

    width, height = pyautogui.size()

    #for i in range(1):
    #      pyautogui.moveTo(300, 300, duration=0.25)
    #      pyautogui.moveTo(400, 300, duration=0.25)
    #      pyautogui.moveTo(400, 400, duration=0.25)
    #      pyautogui.moveTo(300, 400, duration=0.25)
#
    print "Process Complete!......"
    #pyautogui.typewrite("Process Complete!......", 0.25)

    app = Application(backend="uia").start("notepad.exe")
    #app = Application().connect(class_name="Notepad")
    dlg_spec = app['Untitled - Notepad']
    dlg_spec.print_control_identifiers()

    #app.notepad.type_keys("%FX")
#
    #about_dlg = app.window_(title_re = u"关于", class_name = "#32770")
    #app['Untitled - Notepad'].Edit.type_keys('test01')
    #app['Untitled - Notepad'].menu_select("File->Save")
#
    #app['Save As'].Edit.type_keys('test.txt')
    #app['Save As']['Save'].click()
    ##app['确认另存为']['是'].click()
