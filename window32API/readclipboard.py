# coding: utf-8
import win32gui, win32api, win32con
import time
import win32clipboard as w
 
import logging
 
 
def click_position(hwd, x_position, y_position, sleep):
  """
  鼠标左键点击指定坐标
  :param hwd: 
  :param x_position: 
  :param y_position: 
  :param sleep: 
  :return: 
  """
  # 将两个16位的值连接成一个32位的地址坐标
  long_position = win32api.MAKELONG(x_position, y_position)
  # win32api.SendMessage(hwnd, win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP, long_position)
  # 点击左键
  win32api.SendMessage(hwd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
  win32api.SendMessage(hwd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
  time.sleep(int(sleep))
 
 
def getText():
  # 读取剪切板
  w.OpenClipboard()
  d = w.GetClipboardData(win32con.CF_TEXT)
  w.CloseClipboard()
  return d
 
 
def setText(aString):
  # 写入剪切板
  w.OpenClipboard()
  w.EmptyClipboard()
  w.SetClipboardData(win32con.CF_TEXT, aString.encode(encoding='gbk'))
  w.CloseClipboard()
 
 
def input_content(hwd, content, sleep, is_enter):
  """
  从站贴板中查找输入的内容
  :param hwd: 
  :param content: 
  :param sleep: 
  :param is_enter 是否要在最后输入enter键,内容与enter之间间隔一秒
  :return: 
  """
  setText(content)
  time.sleep(0.3)
  click_keys(hwd, win32con.VK_CONTROL, 86)
  if is_enter:
    time.sleep(1)
    click_keys(hwd, win32con.VK_RETURN)
  time.sleep(sleep)
 
 
def click_keys(hwd, *args):
  """
  定义组合按键
  :param hwd: 
  :param args: 
  :return: 
  """
  for arg in args:
    win32api.SendMessage(hwd, win32con.WM_KEYDOWN, arg, 0)
  for arg in args:
    win32api.SendMessage(hwd, win32con.WM_KEYUP, arg, 0)
 
 
def wangwang_operation(hwd, salesname, content1, content2):
  """
  阿里旺旺的操作
  :param hwd: 句柄
  :param salesname: 
  :param content1: 发送一
  :param content2: 发送二
  :return: 
  """
  # 下方联系人标签
  click_position(hwd, 200, 685, 2)
  # 新增好友按钮
  click_position(hwd, 372, 44, 3)
  # 搜索好友
  input_content(hwd, salesname, 3, False)
  # 点击搜索
  click_position(hwd, 345, 117, 5)
  # 点击发送消息
  click_position(hwd, 350, 700, 3)
  # 发送消息一
  input_content(hwd, content1, 1, False)
  click_keys(hwd, win32con.VK_CONTROL, win32con.VK_RETURN)
  time.sleep(1)
  input_content(hwd, content2, 1, False)
  click_keys(hwd, win32con.VK_CONTROL, win32con.VK_RETURN)
  time.sleep(1)
  # 返回原始状态
  click_position(hwd, 20, 45, 1)
  time.sleep(1)
  click_position(hwd, 20, 45, 1)
 
 
def wangwang_operation_by_file(hwd, file, content1, content2):
  with open(file, 'r') as f:
    line = f.readline()
    while len(line) >= 1:
      try:
        line = line.replace('\r', '').replace('\n', '')
        print("正在处理   %s   ....................................." % line)
        wangwang_operation(hwd, line, content1, content2)
        line = f.readline()
      except BaseException as e:
        print("处理 %s 时出错了............." % line)
        logging.exception(e)
 
 
if __name__ == "__main__":
  # 查找句柄
  hwnd = win32gui.FindWindow("Vim", None)
  if int(hwnd) <= 0:
    print("没有找到模拟器，退出进程................")
    exit(0)
  print("查询到模拟器句柄: %s " % hwnd)
  win32gui.MoveWindow(hwnd, 20, 20, 405, 756, True)
  time.sleep(2)
  # 屏幕坐标到客户端坐标
  # print(win32gui.ScreenToClient(hwnd, (1446, 722)))
  # 设置为前台
  # win32gui.SetForegroundWindow(hwnd)
  # 设置为后台
  win32gui.SetBkMode(hwnd, win32con.TRANSPARENT)
  time.sleep(2)
  # 下列的后三个参数分别表示: 文件路径 打招呼句子 广告语
  wangwang_operation_by_file(hwnd, "D:/2.txt", "你好", "测试广告语")