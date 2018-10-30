# -*- coding: utf-8 -*-

import autopy
import time
import win32api
import win32con
#win32api.keybd_event(17,0,0,0)  #ctrl键位码是17
#win32api.SetCursorPos([30,150])    #为鼠标焦点设定一个位置
while (1):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0) 
    print("mouse down 1000")
    #win32api.SetCursorPos([500,500])
    time.sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    print("mouse up 2000")
    time.sleep(16)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0) 
    #win32api.SetCursorPos([500,500])
    print("mouse down 3")
    time.sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    print("mouse up 3")
    time.sleep(5)
    print("mouse down 3")
    win32api.keybd_event(27,0,0,0)

#autopy.alert.alert("hello,world")
##autopy.mouse.move(100, 100) # 移动鼠标
#autopy.mouse.smooth_move(400, 400) # 平滑移动鼠标（上面那个是瞬间的aa）