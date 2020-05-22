#!/usr/bin/env python2
#-*- coding: utf-8 -*-

##############################################################################
# version 1.0:
#   add thread,
#   add ctrl+c to control the quit
#
##############################################################################
"""This script parse stock info"""
 
import tushare as ts
import sys
import pandas as pd
import time
import datetime
import threading
from threading import Event
import signal
import os

import inspect
import ctypes
import itertools
import platform

def get_all_price(code_list):
    '''process all stock'''
    global final_df
    df = ts.get_realtime_quotes(STOCK)
    #print df[['code','price','pre_close','ask','volume','amount','time']]
    #final_df = pd.DataFrame()

    index = 0
    for index in range(0, len(STOCK)):
        final_df = final_df.append(
            pd.DataFrame([[df.loc[index,'code'], 
                df.loc[index,'pre_close'], 
                df.loc[index,'open'], 
                df.loc[index,'price'], 
                df.loc[index,'high'], 
                df.loc[index,'low'], 
                df.loc[index,'time'], 
                format( float(df.loc[index,'price']) * 100 / float(df.loc[index,'pre_close']) - 100, '.2f')]], 
            columns = list(['code', 'pre_close', 'open', 'price', 'high', 'low', 'time', 'rate']) ,
            index=[index]))

    return final_df

class Producer(threading.Thread):
    def run(self):
        global is_exit
        global final_df 
        #final_df = pd.DataFrame()
        while True:
            if cond.acquire():
                if is_exit: #每次获取锁之后，先检查全局状态变量
                    cond.notifyAll() #退出前必须唤醒其他所有线程
                    cond.release() #退出前必须释放锁
                    break
                if len(final_df) > 0:
                    cond.wait()
                else:
                    final_df = get_all_price(STOCK)
                    cond.notify()
                cond.release()

def wait_loop(interval):
    global is_exit
    second_hand = 0
    while True:
        print second_hand,
        time.sleep(2)
        second_hand = second_hand + 2
        if second_hand >= interval: 
            break
        if is_exit == True:
            break
    print second_hand

class Consumer(threading.Thread):
    def run(self):
        global is_exit
        global final_df
        while True:
            if cond.acquire():
                if is_exit:
                    cond.notifyAll()
                    cond.release()
                    break
                if len(final_df) == 0:
                    cond.wait()
                else:
                    sysstr = platform.system()
                    if(sysstr =="Windows"):
                        os.system('cls')
                    elif(sysstr == "Linux"):
                        os.system('clear')
                    else:
                        os.system('clear')

                    print "=========================",datetime.datetime.now(),"=================================="
                    print final_df
                    # after print, need to clear the content in the DataFrame final_df
                    final_df.drop(final_df.index,inplace=True)
                    wait_loop(REPORT_INTERVAL)  # wait 60 seconds to get data
                    cond.notify()
                cond.release()

REPORT_INTERVAL = 60   # wait for one minutes
cond = threading.Condition()
is_exit = False #全局变量

def signal_handler(signum, frame): #信号处理函数
    global is_exit
    is_exit = True #主线程信号处理函数修改全局变量，提示子线程退出
    print "" # make sure below information be printed in a new line
    print "Exit from the process...."


def test():
    global final_df 
    final_df = pd.DataFrame() 
    producers = []
    consumers = []
    for i in xrange(4):
        p = Producer()
        producers.append(p)
        p.setDaemon(True) #子线程daemon
        p.start()
    for j in xrange(2):
        c = Consumer()
        consumers.append(c)
        c.setDaemon(True) #子线程daemon
        c.start()
    while 1:
        alive = False
        for t in itertools.chain(producers, consumers): #循环检查所有子线程
            alive = alive or t.isAlive() #保证所有子线程退出
        if not alive:
            break


STOCK = ['000651',
         '000750',
         '002470',
         '002594',      
         '300119', 
         '600016',
         '600326',       
         '601360',
         '603888'] 
            
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler) #注册信号处理函数
    signal.signal(signal.SIGTERM, signal_handler) #注册信号处理函数
    test()