#!/usr/bin/python
#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------------------#
#   多线程
#   线程池
#-------------------------------------------------------------------------------------------#

'''
所以比较好的方法是维护一个队列，两个线程都从中获取任务，直到把这个队列中的任务都做完。这个过程其实就是特殊的生产消费模式，只不过没有生产者，任务量是固定的而已
'''
import threadingimport requestsfrom bs4 import BeautifulSoupfrom queue import Queueclass MyThread(threading.Thread):    def __init__(self, queue):        threading.Thread.__init__(self)        self.queue = queue    def run(self):        while not self.queue.empty(): # 如果while True 线程永远不会终止            url = self.queue.get()            print(self.name, url)            url_queue.task_done()            r = requests.get(url)            soup = BeautifulSoup(r.content, 'html.parser')            lis = soup.find('ol', class_='grid_view').find_all('li')            for li in lis:                title = li.find('span', class_="title").text                print(title)url_queue = Queue()for i in range(10):    url = 'https://movie.douban.com/top250?start={}&filter='.format(i*25)    url_queue.put(url)th1 = MyThread(url_queue)th2 = MyThread(url_queue)th1.start()th2.start()th1.join()th2.join()url_queue.join()print('finish')

作者：dwzb
链接：https://juejin.im/post/5aa7314e6fb9a028d936d2a4
来源：掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。