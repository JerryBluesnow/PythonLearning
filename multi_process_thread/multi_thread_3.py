#!/usr/bin/python
#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------------------#
#   多线程 - 
#   可重入锁 - 解决同一线程多次获取同一个资源造成的死锁问题
#   mutex = threading.RLock()
#-------------------------------------------------------------------------------------------#
# encoding: UTF-8
import threading
import time

class MyThread(threading.Thread):
    def run(self):
        global num 
        time.sleep(1)

        if mutex.acquire(1):  
            num = num+1
            msg = self.name+' set num to '+str(num)
            print msg
            mutex.acquire()
            mutex.release()
            mutex.release()
num = 0
mutex = threading.RLock()
def test():
    for i in range(5):
        t = MyThread()
        t.start()
if __name__ == '__main__':
    test()