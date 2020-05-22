# -*- coding: utf-8 -*- 

import sys 

import pyautogui
from pywinauto import application

# 读写注册表模块
import _winreg

import os

# 配置参数
pyautogui.PAUSE = 1.5
pyautogui.FAILSAFE = True

# 定义函数
def QueryDnplayerPath():
    '''the function is used to find the installed directory of dnplayer.exe'''
    # 打开注册表
    # cmd --> regedit

    # HKEY_CURRENT_USER/Software/ChangZhi2/dnplayer/InstallDir
    # dnplayer
    # dnmultiplayer.exe 雷电多开器
    try:
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,r"Software\ChangZhi2\dnplayer")

    except WindowsError:
        print "dnplayer isn't installed in the system, please install it before using this script"
        sys.exit(0)   

    try:
        value, type = _winreg.QueryValueEx(key, "InstallDir")
    except WindowsError:
        print "dnplayer InstallDir query failed. not installed in the system, please install it before using this script"
        sys.exit(0)   

    dnplayer_path = value + 'dnmultiplayer.exe'
    print "dnplayer's path:", dnplayer_path

    return dnplayer_path

def StartDnplayer(_dnplayer_path_):
    if _dnplayer_path_ == '':
        print "Invalid Path: ", _dnplayer_path_
        sys.exit(0)

    app = application.Application(backend='win32').start(_dnplayer_path_) 

    return app

if __name__ == '__main__':
    
    # 查找dnplayer.exe安装路径
    dnplayer_path = QueryDnplayerPath()

    # 启动dnplayer.exe
    app = StartDnplayer(dnplayer_path)
    app.window().wait('visible')
    
    #image = pyautogui.screenshot()
    #image.save('testing.png')
    #pyautogui.screenshot(region=(20, 20, 50, 50))

    #sys.exit(0)
    working_path = os.path.abspath('.')

    selectAllButton = None
    while selectAllButton is None:
        print " try ..."
        selectAllButton = pyautogui.locateOnScreen('images_ld/SelectAll.png', grayscale=True)#, confidence=0.999)
        #print "SelectAll.png not matched, quit..."
       #sys.exit(0)   
    
    print "found..."
    
    current_button = selectAllButton
    current_button_x, current_button_y = pyautogui.center(current_button)

    print current_button_x, current_button_y

    pyautogui.moveTo(current_button_x, current_button_y)

    pyautogui.click(current_button_x, current_button_y)

    copyMNQButton = None
    while copyMNQButton is None:
        print " try ..."
        copyMNQButton = pyautogui.locateOnScreen('images_ld/CopyMNQ.png', grayscale=True)

    print "found..."

    current_button = copyMNQButton
    current_button_x, current_button_y = pyautogui.center(current_button)

    print current_button_x, current_button_y

    pyautogui.moveTo(current_button_x, current_button_y)

    pyautogui.click(current_button_x, current_button_y)
    #print app.window(title_re = u'雷电模拟器', class_name = 'LDPlayerMainFrame').print_control_identifiers()
    #print app.window(title_re = u'雷电多开器', class_name = 'LDMultiPlayerMainFrame').print_control_identifiers()
    #dlg_spec = app[u'雷电多开器']
    #dlg_spec.print_control_identifiers()
    
    #app.LDPlayerMainFrame.MenuSelect('软件设置'.decode('gb2312'))
    
    #app[LDPlayerMainFrame]

    #try:
    #    app.connect(u'雷电模拟器')
    #except WindowsError:
    #    print u'could not found 雷电模拟器'
#
    #app.menu_click(window_name,menulist)

    '''
    Control Identifiers:

LDPlayerMainFrame - '雷电模拟器'    (L159, T56, R1761, B994)
[u'\u96f7\u7535\u6a21\u62df\u5668LDPlayerMainFrame', u'LDPlayerMainFrame', u'\u96f7\u7535\u6a21\u62df\u5668']
child_window(title="雷电模拟器", class_name="LDPlayerMainFrame")
   |
   | RenderWindow - 'TheRender'    (L160, T92, R1760, B992)
   | [u'TheRenderRenderWindow', u'TheRender', u'RenderWindow']
   | child_window(title="TheRender", class_name="RenderWindow")
None

    '''
