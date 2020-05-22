# coding: utf-8
import win32gui, win32api, win32con
import time
import win32clipboard as w
 
import logging
 
def isRunning(process_name) :
    try:
        print('tasklist | findstr ' + process_name)
        process=len(os.popen('tasklist | findstr ' + process_name).readlines())
        print(process)
        if process >=1 :
            return True
        else:
            return False
    except:
        print("The application is not running: " + process_name)
        return False

def get_all_hwnd(hwnd, mouse):
    if (win32gui.IsWindow(hwnd)
            and win32gui.IsWindowEnabled(hwnd)
            and win32gui.IsWindowVisible(hwnd)):
      hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

if __name__ == '__main__':
  hwnd = win32gui.FindWindow(None, "同花顺远航版")
  if int(hwnd) <= 0:
    print("没有找到模拟器，退出进程................")
    exit(0)
  print("查询到模拟器句柄: %s " % hwnd)
  win32gui.MoveWindow(hwnd, 20, 20, 405, 756, True)