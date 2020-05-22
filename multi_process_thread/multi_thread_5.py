#!/usr/bin/python
#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------------------#
#   多线程 - 
#   python多线程编程(6): 队列同步
#   https://www.cnblogs.com/holbrook/archive/2012/03/15/2398060.html
#-------------------------------------------------------------------------------------------#
import threading
import time
'''
前面介绍了互斥锁和条件变量解决线程间的同步问题，并使用条件变量同步机制解决了生产者与消费者问题。

让我们考虑更复杂的一种场景：产品是各不相同的。这时只记录一个数量就不够了，还需要记录每个产品的细节。很容易想到需要用一个容器将这些产品记录下来。

Python的Queue模块中提供了同步的、线程安全的队列类，包括FIFO（先入先出)队列Queue，LIFO（后入先出）队列LifoQueue，和优先级队列PriorityQueue。这些队列都实现了锁原语，能够在多线程中直接使用。可以使用队列来实现线程间的同步。

用FIFO队列实现上述生产者与消费者问题的代码如下：
'''
import threading
import time
from Queue import Queue

class Producer(threading.Thread):
    def run(self):
        global queue
        count = 0
        while True:
            for i in range(100):
                if queue.qsize() > 1000:
                     pass
                else:
                     count = count + 1
                     msg = 'Procude Product ' + str(count)
                     queue.put(msg)
                     print msg
                     print ''
            time.sleep(1)

class Consumer(threading.Thread):
    def run(self):
        global queue
        while True:
            for i in range(3):
                if queue.qsize() < 100:
                    pass
                else:
                    msg = self.name + 'Consume Product ' + queue.get()
                    print msg
                    print ''
            time.sleep(1)

queue = Queue()


def test():
    for i in range(500):
        queue.put('initial Product ' + str(i))
    for i in range(2):
        p = Producer()
        p.start()
    for i in range(5):
        c = Consumer()
        c.start()
if __name__ == '__main__':
    test()
