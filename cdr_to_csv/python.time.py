#!/usr/bin/python
#-*- coding: utf-8 -*-

import datetime
import os

if __name__ == "__main__":
    # make 10 seconds as a different, to make it exact in 5
    current_time = datetime.datetime.now()
    current_time.strftime('%m%d%H%M%S')

    second = current_time.strftime('%S')
    minute = current_time.strftime('%M')
    hour = current_time.strftime('%H')

    minute_offset = int(minute) % 5

    if minute_offset == 0 and int(second) < 50:
        print 0
        os._exit(0)
        
    minute_offset = 5 - minute_offset

    wait_seconds = minute_offset * 60 - int(second)

    wait_seconds = wait_seconds + 10
    print wait_seconds