#-*- coding: utf-8 -*-
 
"""This script parse stock info"""
 
import tushare as ts
import sys
import pandas as pd
import time
import datetime

def printChinese(chinese_str):
    type = sys.getfilesystemencoding()
    print chinese_str.decode('UTF-8').encode(type)
    return

def get_all_price(code_list):
    '''process all stock'''
    df = ts.get_realtime_quotes(STOCK)
    #print df[['code','price','pre_close','ask','volume','amount','time']]
    final_df = pd.DataFrame()

    index = 0
    for index in range(0, len(STOCK)):
        final_df = final_df.append(
            pd.DataFrame([[df.loc[index,'code'], 
                df.loc[index,'pre_close'], 
                df.loc[index,'open'], 
                df.loc[index,'price'], 
                df.loc[index,'high'], 
                df.loc[index,'low'], 
                df.loc[index,'time'], 
                format( float(df.loc[index,'price']) * 100 / float(df.loc[index,'pre_close']) - 100, '.2f')]], 
            columns = list(['code', 'pre_close', 'open', 'price', 'high', 'low', 'time', 'rate']) ,
            index=[index]))

    print datetime.datetime.now()
    print final_df

if __name__ == '__main__':
    STOCK = ['600240',      
             '002011',           
             '000651']       
 
    while True:
        get_all_price(STOCK)
        print "==========================================================================="
        time.sleep(60)