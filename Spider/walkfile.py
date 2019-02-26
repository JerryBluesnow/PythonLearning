#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, re, datetime

class Find(object):
    def __init__(self, root, input_file):
        """
             --初始化
        """
        self.root = root  # 文件树的根
        self.input_files = []  # 待查询的字符串集合
        self.files = []  # 待匹配的文件集合
        self.current = 0  # 正在匹配的文件集合的位置

        f = file(input_file, "r")
        old_content = f.read()
        f.close()
        self.input_files = old_content.split('\n')  # 将待匹配字符串保存在数组中

    @staticmethod
    def find_file(self):
        """
        --查找文件，即遍历文件树将查找到的文件放在文件集合中
        :return:
        """
        # python中的walk方法可以查找到所给路径下的所有文件和文件夹，这里只用文件
        for root, dirs, files in os.walk(self.root, topdown=True):
            for name in files:
                self.files.append(os.path.join(root, name))
                #     print(os.path.join(root, name))
                # for name in dirs:
                #     print(os.path.join(root, name))

    @staticmethod
    def walk(self):
        """
        --逐一查找，并将结果存入result.txt文件中
        :param self:
        :return:
        """
        for item1 in self.files:
            Find.traverse_file(self, item1)
        try:
            result = ''
            for item3 in self.input_files:
                result += item3 + '\n'
            f = file("./result_files.txt", "w")
            f.write(result)
            f.close()
        except IOError, msg:
            print "Error:", msg
        else:
            print "OK"

    @staticmethod
    def traverse_file(self, file_path):
        """
        --遍历文件，匹配字符串
        :return:
        """
        f = file(file_path, "r")
        file_content = f.read()
        f.close()
        input_files = []
        for item2 in self.input_files:
            if item2:
                # 正则匹配，不区分大小写
                searchObj = re.search(r'(.*)' + item2 + '.*', file_content, re.M | re.I)
                if searchObj:
                    continue
                else:
                    input_files.append(item2)
        self.input_files = input_files


if __name__ == "__main__":

    print datetime.datetime.now()
    findObj = Find('.', "./input_files.txt")
    findObj.find_file(findObj)
    findObj.walk(findObj)
    print datetime.datetime.now()
