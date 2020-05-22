# coding: utf-8
import win32gui, win32con
import win32api
import win32event
import win32process
import time
import re, traceback
import sys
from time import sleep
import json

'''
cd D:\PythonWorkspace\NewPython3\PythonLearning\window32API
pyinstaller -p D:/Python3/Lib/site-packages -D 2ExecuteMyApp.py
pyinstaller -p D:/Python3/Lib/site-packages -F -w 2ExecuteMyAppDyc.py
pyinstaller -p D:/Python3/Lib/site-packages -F -w 2ExecuteMyAppDyc.py
python 2ExecuteMyAppDyc.py "同花顺远航版" "D:\\Program Files (x86)\\ths\\THS\\hstart.exe" "MAX"
./2ExecuteMyAppDyc.exe "同花顺远航版" "D:\\Program Files (x86)\\ths\\THS\\hstart.exe" "MAX"
'''

class cWindow:
    def __init__(self):
        self._hwnd = None
    def SetAsForegroundWindow(self):
        # First, make sure all (other) always-on-top windows are hidden.
        self.hide_always_on_top_windows()
        win32gui.SetForegroundWindow(self._hwnd)
    def Maximize(self):
        win32gui.ShowWindow(self._hwnd, win32con.SW_MAXIMIZE)
    def Minimize(self):
        win32gui.ShowWindow(self._hwnd, win32con.SW_MINIMIZE)
    def setSize(self, sizemode):
        if sizemode == win32con.SW_MINIMIZE:
            self.Minimize()
        elif  sizemode == win32con.SW_MAXIMIZE:
            self.Maximize()
            self.SetAsForegroundWindow()
    def _window_enum_callback(self, hwnd, regex):
        '''Pass to win32gui.EnumWindows() to check all open windows'''
        if self._hwnd is None and re.match(regex, str(win32gui.GetWindowText(hwnd))) is not None:
            self._hwnd = hwnd
    def find_window_regex(self, regex):
        self._hwnd = None
        win32gui.EnumWindows(self._window_enum_callback, regex)
    def hide_always_on_top_windows(self):
        win32gui.EnumWindows(self._window_enum_callback_hide, None)
    def _window_enum_callback_hide(self, hwnd, unused):
        if hwnd != self._hwnd: # ignore self
            # Is the window visible and marked as an always-on-top (topmost) window?
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & win32con.WS_EX_TOPMOST:
                # Ignore windows of class 'Button' (the Start button overlay) and
                # 'Shell_TrayWnd' (the Task Bar).
                className = win32gui.GetClassName(hwnd)
                if not (className == 'Button' or className == 'Shell_TrayWnd'):
                    # Force-minimize the window.
                    # Fortunately, this seems to work even with windows that
                    # have no Minimize button.
                    # Note that if we tried to hide the window with SW_HIDE,
                    # it would disappear from the Task Bar as well.
                    win32gui.ShowWindow(hwnd, win32con.SW_FORCEMINIMIZE)
    def startApp(self, path, sizemode):
        if self._hwnd is None:
            startinfo = win32process.STARTUPINFO()
            startinfo.wShowWindow = sizemode
            info  = win32process.CreateProcess(None, path, None, None, 0, 0, None, None, startinfo)
            subprocess = info [0]
            rc = win32event.WaitForSingleObject (subprocess, win32event.INFINITE)
            if rc == win32event.WAIT_TIMEOUT:
                try:
                    win32process.TerminateProcess (subprocess, 0)                   
                except pywintypes.error:
                    return -3
                return -2
            if rc == win32event.WAIT_OBJECT_0:
                return win32process.GetExitCodeProcess(subprocess)
def main():
    app_data = {}
    app_data['Application Name'] = sys.argv[1]
    app_data['Application Path'] = sys.argv[2]
    app_data['Application Size'] = sys.argv[3]
    print(app_data['Application Path'])
    print(app_data['Application Name'])
    print(app_data['Application Size'])
    
    sizemode = win32con.SW_MAXIMIZE
    if app_data['Application Size'] == "MAX":
        sizemode = win32con.SW_MAXIMIZE
    elif app_data['Application Size'] == "MIN":
        sizemode = win32con.SW_MINIMIZE

    try:
        regex = ".*" + app_data['Application Name'] + ".*"
        cW = cWindow()
        cW.find_window_regex(regex)
        if cW._hwnd is None:
            cW.startApp(app_data['Application Path'], sizemode)
        else:
            cW.setSize(sizemode)
    except:
        f = open("log.txt", "w")
        f.write(traceback.format_exc())
        print(traceback.format_exc())
main()