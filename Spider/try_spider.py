#!/usr/bin/python
#-*- coding: utf-8 -*-
import urllib2
from urllib2 import urlopen

# get all content of the wabpage
def askURL(url):
    request = urllib2.Request(url) # send request
    try:
        response = urllib2.urlopen(request) # get response from the request
        html= response.read() # get webpage content
        print html
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    return html



def main():
    #html = urlopen('https://mp.weixin.qq.com')
    askURL('https://mp.weixin.qq.com')
main()