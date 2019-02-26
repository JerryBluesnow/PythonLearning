#!/usr/bin/python
# -*- coding: UTF-8 -*-

#[python中得到shell命令输出的方法](https://blog.csdn.net/wanglei_storage/article/details/54615952)

# usage: python walkpath.py /directory/ searched_string
#        python ~/walkpath.py  $OFROOT/glob/ obj ssp csp
#        the script is used to list all files in the pointed path, 
#        but could exlude the files in the pointed path
#        in the above example, files in obj ssp csp dir and subdir will be excluded.

import os, re, datetime
import sys

if __name__ == "__main__":
    print datetime.datetime.now()
    search_path = sys.argv[1]
    print "execute script", sys.argv[0], "with", len(sys.argv), "arguments, searched path:", search_path

    argv_idx = 2
    subpath_filter = []
    while argv_idx < len(sys.argv):
        subpath_filter.append(sys.argv[argv_idx])
        argv_idx = argv_idx + 1

    fileList = []

    for filename in os.listdir(search_path):
        if filename in subpath_filter:
            print os.path.join(search_path, filename), "is excluded......"
            continue
        filepath = os.path.join(search_path, filename)
        if os.path.isfile(filepath):
            fileList.append(filepath)
            print filepath
        else:
            for root, dirs, files in os.walk(filepath):
                    for name in files:
                        print(os.path.join(root, name))


