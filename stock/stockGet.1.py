#-*- coding: utf-8 -*-
 
"""This script parse stock info"""
 
import tushare as ts
import sys


def printChinese(chinese_str):
    type = sys.getfilesystemencoding()
    print chinese_str.decode('UTF-8').encode(type)
    return

def get_all_price(code_list):
    '''process all stock'''
    df = ts.get_realtime_quotes(STOCK)
    print df
 
if __name__ == '__main__':
    STOCK = ['600219',       ##南山铝业
             '000002',       ##万  科Ａ
             '000623',       ##吉林敖东
             '000725',       ##京东方Ａ
             '600036',       ##招商银行
             '601166',       ##兴业银行
             '600298',       ##安琪酵母
             '600881',       ##亚泰集团
             '002582',       ##好想你
             '600750',       ##江中药业
             '601088',       ##中国神华
             '000338',       ##潍柴动力
             '000895',       ##双汇发展
             '000792']       ##盐湖股份
 
    get_all_price(STOCK)
