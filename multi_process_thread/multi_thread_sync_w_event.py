#!/usr/bin/python
#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------------------#
#  参考线程间的通讯– event：http://zhaochj.github.io/2016/08/14/2016-08-14-%E7%BA%BF%E7%A8%8B%E7%9A%84event%E7%89%B9%E6%80%A7/
#-------------------------------------------------------------------------------------------#
import threading
import logging
import time
 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s')
 
def worker(event):
    while not event.is_set():
        event.wait(timeout=1)
        logging.debug('in worker fun, event is set ? {0}'.format(event.is_set()))
    logging.debug('event is set')
 
 
def set(event):
    time.sleep(4)
    event.set()
    logging.debug('in set fun, event is set ? {0}'.format(event.is_set()))
 
if __name__ == '__main__':
    event = threading.Event()
    w = threading.Thread(target=worker, args=(event,), name="worker")
    w.start()
    s = threading.Thread(target=set, args=(event,), name="set")
    s.start()
