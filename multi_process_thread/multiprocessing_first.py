#-*- coding: utf-8 -*-

import multiprocessing
from multiprocessing import Process
from time import sleep
import time


class MultiProcessProducer(multiprocessing.Process):
   def __init__(self, num, queue):
      """Constructor"""
      multiprocessing.Process.__init__(self)
      self.num = num
      self.queue = queue

   def run(self):
      t1 = time.time()
      print('producer start ' + str(self.num))
      for i in range(1000):
         self.queue.put((i, self.num))
      # print 'producer put', i, self.num
      t2 = time.time()

      print('producer exit ' + str(self.num))
      use_time = str(t2 - t1)
      print('producer ' + str(self.num) + ', use_time: '+ use_time)



class MultiProcessConsumer(multiprocessing.Process):
   def __init__(self, num, queue):
      """Constructor"""
      multiprocessing.Process.__init__(self)
      self.num = num
      self.queue = queue

   def run(self):
      t1 = time.time()
      print('consumer start ' + str(self.num))
      while True:
         d = self.queue.get()
         if d != None:
            # print 'consumer get', d, self.num
            continue
         else:
            break
      t2 = time.time()
      print('consumer exit ' + str(self.num))
      print('consumer ' + str(self.num) + ', use time:' + str(t2 - t1))


def main():
   # create queue
   queue = multiprocessing.Queue()

   # create processes
   producer = []
   for i in range(5):
      producer.append(MultiProcessProducer(i, queue))

   consumer = []
   for i in range(5):
      consumer.append(MultiProcessConsumer(i, queue))

   # start processes
   for i in range(len(producer)):
      producer[i].start()

   for i in range(len(consumer)):
      consumer[i].start()

   # wait for processs to exit
   for i in range(len(producer)):
      producer[i].join()

   for i in range(len(consumer)):
      queue.put(None)

   for i in range(len(consumer)):
      consumer[i].join()

   print('all done finish')


if __name__ == "__main__":
   main()