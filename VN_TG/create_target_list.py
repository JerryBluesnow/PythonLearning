#-*- coding: utf-8 -*-

import sys
import os
from optparse import OptionParser

if __name__ == "__main__":
    '''All parameters are mandatory, please make sure they are used'''
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-s", "--sourcestring", dest="sourcestring",
                      help="input source string")
    parser.add_option("-a", "--appendstring", dest="appendstring",
                      help="append the appendstring to sourcestring")
    (options, args) = parser.parse_args()

    source_string = options.sourcestring
    append_string = options.appendstring
    #source_string = source_string + append_string
    #source_string = source_string + append_string

    try:
        tmp_fo = open('tmp_list_data.txt', "a")
        tmp_fo.write(source_string)
    except IOError:
        print "failed to open tmp_list_data.txt"

    #print source_string 
    tmp_fo.close()