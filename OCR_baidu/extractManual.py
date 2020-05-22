#-*- coding: utf-8 -*-

import os
from aip import AipOcr
from optparse import OptionParser

APP_ID = '15616936'
API_KEY = 'Z17flg6kNjPFnMAplvB8UZfp'
SECRET_KEY = 'wuUmiwP9oH29lXphEguQFNYq1GZrrNbq'

# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def main():
    '''Not all parameters are mandatory, please make sure they are used'''
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--path", dest="path", default='',
                      help="the directory stored the images to be recognized")
    parser.add_option("-f", "--file", dest="file", default='',
                      help="the isolate file to be recongnized")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quit",
                      action="store_false", dest="verbose")

    (options, args) = parser.parse_args()

    print options.path, options.file

    if len(options.path) == 0 and  len(options.file) == 0:
        print 'exit, without path and file input'
        return 

    if len(options.path) > 0 and  len(options.file) > 0:
        print 'exit, with both path and file input'
        return 

    # 初始化ApiOcr对象
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    if len(options.path) > 0:
        if not os.path.isdir(options.path):
            print 'exit, input path is not a directory'
            return 

        ocr_w_path_input(client, options.path)

    if len(options.file) > 0:
        if not os.path.isfile(options.file):
            print 'exit, input is not a file'
            return 

        ocr_w_file_input(client, options.file)
    
    return

def ocr_w_path_input(_client, _path):
    file_list = os.listdir(_path)
    for filename in file_list:
        ocr_w_file_input(_client, _path + os.path.sep + _file_name)
    
    print "ocr in path complete...."
    return

def ocr_w_file_input(_client, _file_name):
    try:
        result = _client.basicGeneral(get_file_content(_file_name))

        print 'for file:', _file_name, len(result[u'words_result']), 'generated'
        for items in result[u'words_result']:
            print items[u'words'].decode('utf-8')
    except:
        print "nothing generated"
    
    return

if __name__ == "__main__":
    main()