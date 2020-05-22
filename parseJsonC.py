# encoding:utf-8
import json
import re
import sys
import os.path
from optparse import OptionParser

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError, e:
        return False
    return True

def menu():
    parser = OptionParser(usage = '''''')
    parser.add_option('-f', '--file', dest='file', action='store',
        help="master log")
    parser.add_option('-r', '--regex', dest='regex', action='store_true',
        help="use regular express to match, instead of the default 'glob'")
    parser.add_option('-v', '--invert',dest='invert',action='store_true',
        help="invert the logic. (match is not match, vice versa)")
    parser.add_option('-t', '--topline', dest='topline', action='store',
        help="HTTP message topline")
    parser.add_option('-p', '--param', dest='param', action='store',
        help="searched key")
    parser.add_option('-H', '--Header', dest='header', action='store',
        help="searched header")

    (options, args) = parser.parse_args()

    if not options.file or not os.path.exists(options.file):
        print("invalid input log file, please check:")
        sys.exit(1)

    if not options.topline:
        print("invalid input topline, please check:" + options.file)
        sys.exit(1)
    
    return options.file, options.topline, options.param, options.header

def parseHTTPJsonContent(file, topline, param):
    with open(file) as file_obj:
        contents = file_obj.read()
        json_content = re.findall(topline + '.*HTTP/1.1.*[\r\n](.*^{.*[\r\n]^})', contents, re.S|re.M)
        if not json_content:
            print("Unmatched")
            sys.exit()
        json2parse = json_content[0].replace('\r', '').replace('\n', '')
        #print(json_content[0])
        if is_json(json2parse) == False:
            print("invalid Json Format")
            sys.exit()
        strDict = json.loads(json2parse)
        search_str = param.split('.')
        if len(search_str) == 1:
            if search_str[0] not in strDict.keys():
                print("Invalid Key:" + search_str[0])
                sys.exit(0)
            print(strDict[search_str[0]])

        elif len(search_str) == 2:
            if search_str[0] not in strDict.keys():
                print("Invalid Key:" + search_str[0])
                sys.exit(0)
            if search_str[1] not in strDict[search_str[0]].keys():
                print("Invalid Key:" + search_str[1])
                sys.exit(0)
            print(strDict[search_str[0]][search_str[1]])

        elif len(search_str) == 3:
            if search_str[0] not in strDict.keys():
                print("Invalid Key:" + search_str[0])
                sys.exit(0)
            if search_str[1] not in strDict[search_str[0]].keys():
                print("Invalid Key:" + search_str[1])
                sys.exit(0)
            if search_str[2] not in strDict[search_str[0]][search_str[1]].keys():
                print("Invalid Key:" + search_str[2])
                sys.exit(0)
            print(strDict[search_str[0]][search_str[1]][search_str[2]])

        elif len(search_str) == 4:
            if search_str[0] not in strDict.keys():
                print("Invalid Key:" + search_str[0])
                sys.exit(0)
            if search_str[1] not in strDict[search_str[0]].keys():
                print("Invalid Key:" + search_str[1])
                sys.exit(0)
            if search_str[2] not in strDict[search_str[0]][search_str[1]].keys():
                print("Invalid Key:" + search_str[2])
                sys.exit(0)
            if search_str[3] not in strDict[search_str[0]][search_str[1]][search_str[2]].keys():
                print("Invalid Key:" + search_str[2])
                sys.exit(0)
            print(strDict[search_str[0]][search_str[1]][search_str[2]][search_str[3]])

def parseHTTPHeader(file, topline, param, header):
    match_str = topline + '.*HTTP\/1.1.*[\r\n]?'+ header +':'+'(.*$)(.*^{.*[\r\n]^})'
    with open(file) as file_obj:
        contents = file_obj.read()
        json_content = re.findall(match_str, contents, re.S|re.M)
        if not json_content:
            print("Unmatched")
            sys.exit()
        print(json_content[0])

if __name__ == '__main__':
    file, topline, param, header = menu()

    if header:
        parseHTTPHeader(file, topline, param, header)
        sys.exit(0)
    
    parseHTTPJsonContent(file, topline, param)
    sys.exit(0)