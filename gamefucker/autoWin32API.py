# -*- coding: utf-8 -*-


# reference: 
#
# [python win32api win32gui win32con 简单操作教程（窗口句柄 发送消息 常用方法 键盘输入)](https://blog.csdn.net/qq_16234613/article/details/79155632)
# 
# [Python win32gui Module](https://www.programcreek.com/python/index/322/win32gui)
#

import win32gui
import win32con
import win32api

import pyautogui

# 从顶层窗口向下搜索主窗口，无法搜索子窗口
# FindWindow(lpClassName=None, lpWindowName=None)  窗口类名 窗口标题名
handle = None

try:
    handle = win32gui.FindWindow('LDPlayerMainFrame', None)

except WindowsError:
    print "dnplayer InstallDir query failed. not installed in the system, please install it before using this script"
    sys.exit(0)   

# 获取窗口位置
left, top, right, bottom = win32gui.GetWindowRect(handle)
#获取某个句柄的类名和标题
title = win32gui.GetWindowText(handle)     
clsname = win32gui.GetClassName(handle)

print 'Title of  ldplayer:', title
print 'Class of  ldplayer:', clsname

# 十进制
print 'Handle of ldplayer:',"%x" %(handle)

# 搜索子窗口
# 枚举子窗口
hwndChildList = []     
win32gui.EnumChildWindows(handle, lambda hwnd, param: param.append(hwnd),  hwndChildList)

print 'Child Windows:', hwndChildList

menuHandle = win32gui.GetMenu(handle)

print menuHandle

my_window = pyautogui.getWindow(u'雷电模拟器') 
print my_window
my_window.resize(400, 400)
my_window.moveRel(x=0, y=0)