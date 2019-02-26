#!/usr/bin/python
# -*- coding: UTF-8 -*-

#[python中得到shell命令输出的方法](https://blog.csdn.net/wanglei_storage/article/details/54615952)

# usage: python walkfile2.py /directory/ searched_string
#        python ~/walkfile2.py  $OFROOT/glob/ LU3P.include out cpp c h out1 out2 out3 out4

import os, re, datetime
import sys

if __name__ == "__main__":
    print datetime.datetime.now()
    search_path = sys.argv[1]
    search_string = sys.argv[2]
    print "execute script", sys.argv[0], "with", len(sys.argv), "arguments, searched path:", search_path,"searched string:", search_string

    argv_idx = 3
    type_filter = []
    while argv_idx < len(sys.argv):
        type_filter.append(sys.argv[argv_idx])
        argv_idx = argv_idx + 1

    for fpathe, dirs, fs in os.walk(search_path):
        for f in fs:
            if os.path.splitext(f)[-1][1:] in type_filter:
                print ".",
                continue
            file_found = os.path.join(fpathe,f)
            process = os.popen('grep ' + search_string + ' ' + file_found) # return file
            output = process.read()
            process.close()
            if len(output) != 0:
                print ""
                print "==============================", file_found, "=========================================================================================="
                print output
            else:
                print ".",
    print datetime.datetime.now()


