#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
import urllib2
import re
import time
from bs4 import BeautifulSoup
def get_html(url):  #通过url获取网页内容
    result = urllib2.urlopen(url)
    return result.read()

    # save_file(result.read(), 'thefile.txt')
def get_movie_all(html):     #通过soup提取到每个电影的全部信息，以list返回
    soup = BeautifulSoup(html)
    movie_list = soup.find_all('div', class_='bd doulist-subject')
    return movie_list

def get_movie_one(movie):
    result = []  # 用于存储提取出来的电影信息
    soup_all = BeautifulSoup(str(movie))
    title = soup_all.find_all('div', class_='title')
    soup_title = BeautifulSoup(str(title[0]))
    for line in soup_title.stripped_strings:  # 对获取到的<a>里的内容进行提取
        result.append(line)

    # num = soup_all.find_all('span', class_='rating_nums')
    num = soup_all.find_all('span')
    result.append(num[1].contents[0])

    soup_num = BeautifulSoup(str(num[0]))
    for line in soup_num.stripped_strings:  # 对获取到的<span>里的内容进行提取
        result = result + line

    info = soup_all.find_all('div', class_='abstract')
    soup_info = BeautifulSoup(str(info[0]))
    result_str = ""
    for line in soup_info.stripped_strings:  # 对获取到的<div>里的内容进行提取
        result_str = result_str + line
    result.append(result_str)
    return result  #返回获取到的结果

def save_file(text, filename):  #保存网页到文件
    f= open(filename,'ab')
    f.write(text)
    f.close()
    
def read_file(filename):  #读取文件
    f = open(filename,'r')
    text = f.read()
    f.close()
    return text

if __name__=='__main__':
    print "strvice start..."
    for i in range(0,426,25):
        url = 'https://www.douban.com/doulist/3516235/?start='+str(i)+'&sort=seq&sub_type='
        print "Now URI is :"
        print url
        html = get_html(url)
        movie_list = get_movie_all(html)
        for movie in movie_list:  #将每一页中的每个电影信息放入函数中提取
            print "go to get movie............................................"
            result = get_movie_one(movie)
            text = ''+'电影名：'+str(result[0])+' | 评分：'+str(result[1])+' | '+str(result[2])+'\n'+'\t'
            print text
            save_file(text,'thee.txt')
        time.sleep(5)  #每隔5秒抓取一页的信息
    
