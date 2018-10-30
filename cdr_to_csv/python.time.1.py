#!/usr/bin/python
#-*- coding: utf-8 -*-

import datetime
import os

PREFIX_NAME=''
SUFFIX_NAME=''
UP_WAIT_SECONDS=0
DOWN_WAIT_SECONDS=0
#A20181019.0145+0800-0200+0800_ManagedElement=lcp-1

INTERVAL_TIME=5

SECONDS_IN_MINUTE=60

if __name__ == "__main__":
    # make 10 seconds as a different, to make it exact in 5
    print "the script is used to make sure the scenario will be finished in not than 3.5 minutes in 5 interval"
    current_timestamp = datetime.datetime.now()
    current_timestamp.strftime('%m%d%H%M%S')

    second = current_timestamp.strftime('%S')
    minute = current_timestamp.strftime('%M')
    hour = current_timestamp.strftime('%H')

    minute_offset = int(minute) % INTERVAL_TIME

    if minute_offset == 0:
        up_timestamp = current_timestamp
        down_timestamp = up_timestamp + datetime.timedelta(minutes=INTERVAL_TIME)

        PREFIX_NAME = 'A' + up_timestamp.strftime('%Y%m%d') + '.' + up_timestamp.strftime('%H%M')
        SUFFIX_NAME = down_timestamp.strftime('%H%M')

        UP_WAIT_SECONDS = 0 * SECONDS_IN_MINUTE

        DOWN_WAIT_SECONDS = (INTERVAL_TIME - 0) * SECONDS_IN_MINUTE - int(second)

    elif minute_offset == 1:
        up_timestamp = current_timestamp + datetime.timedelta(minutes=(0 - minute_offset))
        down_timestamp = up_timestamp + datetime.timedelta(minutes=INTERVAL_TIME)

        PREFIX_NAME = 'A' + up_timestamp.strftime('%Y%m%d') + '.' + up_timestamp.strftime('%H%M')
        SUFFIX_NAME = down_timestamp.strftime('%H%M')

        UP_WAIT_SECONDS = 0 * SECONDS_IN_MINUTE

        DOWN_WAIT_SECONDS = (INTERVAL_TIME - minute_offset) * SECONDS_IN_MINUTE - int(second)
    else:
        up_timestamp = current_timestamp + datetime.timedelta(minutes=(INTERVAL_TIME - minute_offset))
        down_timestamp = up_timestamp + datetime.timedelta(minutes=INTERVAL_TIME)

        PREFIX_NAME = 'A' + up_timestamp.strftime('%Y%m%d') + '.' + up_timestamp.strftime('%H%M')
        SUFFIX_NAME = down_timestamp.strftime('%H%M')

        UP_WAIT_SECONDS = (INTERVAL_TIME - minute_offset) * SECONDS_IN_MINUTE - int(second)

        DOWN_WAIT_SECONDS = INTERVAL_TIME * SECONDS_IN_MINUTE + UP_WAIT_SECONDS

    print "PREFIX_NAME=%s" % PREFIX_NAME
    print "SUFFIX_NAME=%s" % SUFFIX_NAME
    print "UP_WAIT_SECONDS=%d" % UP_WAIT_SECONDS
    print "DOWN_WAIT_SECONDS=%d" % DOWN_WAIT_SECONDS