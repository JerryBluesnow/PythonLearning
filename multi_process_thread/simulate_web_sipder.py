#!/usr/bin/python
#-*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------#
#  
#-------------------------------------------------------------------------------------------#

import threading # 导入线程包
import time

detail_url_list = []
# 爬取文章详情页
def get_detail_html(detail_url_list, id):
    while True:
        if len(detail_url_list)==0: # 列表中为空，则等待另一个线程放入数据
            continue
        url = detail_url_list.pop()
        time.sleep(2)  # 延时2s，模拟网络请求
        print("thread {id}: get {url} detail finished".format(id=id,url=url))

# 爬取文章列表页
def get_detail_url(detail_url_list):
    for i in range(10000):
        time.sleep(1) # 延时1s，模拟比爬取文章详情要快
        detail_url_list.append("http://projectedu.com/{id}".format(id=i))
        print("get detail url {id} end".format(id=i))

if __name__ == "__main__":
    # 创建读取列表页的线程
    thread = threading.Thread(target=get_detail_url, args=(detail_url_list,))
    # 创建读取详情页的线程
    html_thread= []
    for i in range(4):
        thread2 = threading.Thread(target=get_detail_html, args=(detail_url_list,i))
        html_thread.append(thread2)
    start_time = time.time()
    # 启动两个线程
    thread.start()
    for i in range(4):
        html_thread[i].start()
    # 等待所有线程结束
    thread.join()
    for i in range(4):
        html_thread[i].join()

    print("last time: {} s".format(time.time()-start_time))