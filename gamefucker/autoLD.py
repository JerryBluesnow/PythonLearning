# -*- coding: utf-8 -*- 

import sys 

import pyautogui
from pywinauto import application

# 读写注册表模块
import _winreg


def QueryDnplayerPath():
    '''the function is used to find the installed directory of dnplayer.exe'''
    # 打开注册表
    # cmd --> regedit

    # HKEY_CURRENT_USER/Software/ChangZhi2/dnplayer/InstallDir
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

    dnplayer_path = value + 'dnplayer.exe'
    print "dnplayer's path:", dnplayer_path

    return dnplayer_path

def StartDnplayer(_dnplayer_path_):
    if _dnplayer_path_ == '':
        print "Invalid Path: ", _dnplayer_path_
        sys.exit(0)

    app = application.Application().start(_dnplayer_path_) 

    return app

if __name__ == '__main__':
    
    # 查找dnplayer.exe安装路径
    dnplayer_path = QueryDnplayerPath()

    # 启动dnplayer.exe
    app = StartDnplayer(dnplayer_path)

    print app.window()

    print app.window().print_control_identifiers()

    #app.LDPlayerMainFrame.MenuSelect('软件设置'.decode('gb2312'))
    

    