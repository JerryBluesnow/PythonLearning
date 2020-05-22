#!/usr/bin/python
#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------------------#
#   Python并发编程之线程池/进程池
#   https://segmentfault.com/a/1190000007926055#articleHeader3
#   使用submit操作回顾
#-------------------------------------------------------------------------------------------#

'''
'''
# example3.py
import concurrent.futures
import urllib2

URLS = ['http://httpbin.org', 'http://example.com/', 'https://api.github.com/']

def load_url(url, timeout):
    with urllib2.urlopen(url, timeout=timeout) as conn:
        return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))