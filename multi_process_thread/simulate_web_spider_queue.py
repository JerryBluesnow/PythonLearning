#!/usr/bin/python
#-*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------#
#  use Queue to replace global variable for multi-thread sync
#  Queue is thread-safe 
#-------------------------------------------------------------------------------------------#
import threading # 导入线程包
import Queue as queue
import time

# 爬取文章详情页
def get_detail_html(detail_url_list, id):
    while True:
        url = detail_url_list.get()
        time.sleep(0.2)  # 延时0.2s，模拟网络请求
        print("thread {id}: get {url} detail finished".format(id=id,url=url))

# 爬取文章列表页
def get_detail_url(queue):
    for i in range(500):
        time.sleep(0.1) # 延时0.1s，模拟比爬取文章详情要快
        queue.put("http://projectedu.com/{id}".format(id=i))
        print("get detail url {id} end".format(id=i))

if __name__ == "__main__":
    detail_url_queue = queue.Queue(maxsize=1000)
    # 先创造两个线程
    thread = threading.Thread(target=get_detail_url, args=(detail_url_queue,))
    html_thread= []
    for i in range(3):
        thread2 = threading.Thread(target=get_detail_html, args=(detail_url_queue,i))
        html_thread.append(thread2)
    start_time = time.time()
    # 启动两个线程
    thread.start()
    for i in range(3):
        html_thread[i].start()
    # 等待所有线程结束
    thread.join()
    for i in range(3):
        html_thread[i].join()

    print("last time: {} s".format(time.time()-start_time))