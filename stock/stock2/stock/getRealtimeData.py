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
'''
class Watcher():
 
    def __init__(self):
        self.child = os.fork()
        if self.child == 0:
            return
        else:
            self.watch()
 
    def watch(self):
        try:
            os.wait()
        except KeyboardInterrupt:
            self.kill()
        sys.exit()
 
    def kill(self):
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError:
            pass
'''
def printChinese(chinese_str):
    type = sys.getfilesystemencoding()
    print chinese_str.decode('UTF-8').encode(type)
    return

def get_all_price(code_list):
    '''process all stock'''
    print "going to get realtime data @", datetime.datetime.now(), ", be patient..."
    df = ts.get_realtime_quotes(STOCK)
    print "get done, @",datetime.datetime.now()
    #print df[['code','price','pre_close','ask','volume','amount','time']]
    final_df = pd.DataFrame()

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

    #print datetime.datetime.now()
    print final_df

def worker(self_event, event_obj, input_list):
    while True:
        self_event.clear()
        event_obj.wait()
        get_all_price(input_list)
        self_event.set()

def wait_time_signal(seconds):
    print 'start timer watch with', seconds, 'seconds'
    for i in range(0, seconds):
        print '.',
        time.sleep(1)
    print '.'
    print 'stop timer watch...'

def process(self_event, event_obj):
    while True:
        event_obj.wait()
        self_event.clear()
        wait_time_signal(60)
        self_event.set()

def quit(signum, frame):
    print 'Ctrl+C is pressed to stop the process.'
    sys.exit()

if __name__ == '__main__':

    STOCK = ['600240',      
             '002230',           
             '000651']       
    
    try:
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)

        time_event = Event()
        work_event = Event()

        worker_thread = threading.Thread(target=worker, args=(work_event,time_event, STOCK))
        process_thread = threading.Thread(target=process, args=(time_event,work_event))

        #worker_thread.setDaemon(True)
        #process_thread.setDaemon(True)
        worker_thread.start()
        process_thread.start()

        print "set signal to start..."
        time_event.set()

    except Exception, exc:
        print exc
