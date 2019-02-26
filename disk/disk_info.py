#!/usr/bin/python
#-*- coding: utf-8 -*-

import os

def disk_stat(folder):
    """
    查看文件夹占用磁盘信息
    :param folder: 文件夹路径
    :return:
    """
    hd={}
    disk = os.statvfs(folder)
    print(disk)
    # 剩余
    hd['free'] = disk.f_bavail * disk.f_frsize
    # 总共
    hd['total'] = disk.f_blocks * disk.f_frsize
    # 已使用
    hd['used'] = hd['total'] - hd['free']
    # 使用比例
    hd['used_proportion'] =  float(hd['used']) / float(hd['total'])

    return hd


if __name__ == "__main__":
    hd = disk_stat('./')

    print hd['used_proportion'] 