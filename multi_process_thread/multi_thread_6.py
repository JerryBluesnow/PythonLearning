#!/usr/bin/python
#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------------------#
#   多线程 - 
#   python多线程编程(7):线程间通信
#   https://www.cnblogs.com/holbrook/archive/2012/03/21/2409031.html
#-------------------------------------------------------------------------------------------#

'''
很多时候，线程之间会有互相通信的需要。常见的情形是次要线程为主要线程执行特定的任务，在执行过程中需要不断报告执行的进度情况。前面的条件变量同步已经涉及到了线程间的通信（threading.Condition的notify方法）。更通用的方式是使用threading.Event对象。
threading.Event可以使一个线程等待其他线程的通知。其内置了一个标志，初始值为False。线程通过wait()方法进入等待状态，直到另一个线程调用set()方法将内置标志设置为True时，Event通知所有等待状态的线程恢复运行。还可以通过isSet()方法查询Envent对象内置状态的当前值。
'''
import threading
import random
import time

class MyThread(threading.Thread):
    def __init__(self,threadName,event):
        threading.Thread.__init__(self,name=threadName)
        self.threadEvent = event

    def run(self):
        print "%s is ready" % self.name
        self.threadEvent.wait()
        print "%s run!" % self.name

sinal = threading.Event()
for i in range(10):
    t = MyThread(str(i), sinal)
    t.start()

sinal.set()