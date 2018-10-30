1. 安装tushare
    pip install tushare
2. https://blog.csdn.net/rytyy/article/details/78113373
https://blog.csdn.net/weixin_37450657/article/details/78789673
http://tushare.waditu.com/trading.html
https://blog.csdn.net/xieyan0811/article/details/75635780
https://blog.csdn.net/lanchunhui/article/details/52914466
https://download.csdn.net/download/qq_39579696/9994271
https://blog.csdn.net/cf406061841/article/details/79278685
https://blog.csdn.net/wu__di/article/details/79370056
http://quote.eastmoney.com/stocklist.html#sz
https://www.cnblogs.com/DreamRJF/p/8660630.html

阅读数：147
使用matplotlib和tushare绘制K线与成交量组合图

http://blog.csdn.net/u014281392/article/details/73611624

tushare应用小实例

http://blog.csdn.net/robertsong2004/article/details/50643198

使用tushare获取股票历史行情数据并导入数据库（后复权及未复权）

http://blog.csdn.net/hualugu_6/article/details/54944248?locationNum=1&fps=1

tushare获取数据并存入excel数据表

http://blog.csdn.net/elite666/article/details/62882229?locationNum=1&fps=1

使用tushare开发股票分析脚本

http://blog.csdn.net/stpenghui/article/details/75980032?locationNum=3&fps=1#-*- coding: utf-8 -*-

import tushare as ts
import sys

from openpyxl.reader.excel import load_workbook
import json


wb = load_workbook(filename=r'D:/PythonWorkplace/PythonLearning/stock/stock_s.xlsx')

print "Worksheet range(s):", wb.get_named_ranges()
print "Worksheet name(s):", wb.get_sheet_names()

def printChinese(chinese_str):
    type = sys.getfilesystemencoding()
    print chinese_str.decode('UTF-8').encode(type)

printChinese ("date:日期")阅读数：147
使用matplotlib和tushare绘制K线与成交量组合图

http://blog.csdn.net/u014281392/article/details/73611624

tushare应用小实例

http://blog.csdn.net/robertsong2004/article/details/50643198

使用tushare获取股票历史行情数据并导入数据库（后复权及未复权）

http://blog.csdn.net/hualugu_6/article/details/54944248?locationNum=1&fps=1

tushare获取数据并存入excel数据表

http://blog.csdn.net/elite666/article/details/62882229?locationNum=1&fps=1

使用tushare开发股票分析脚本

http://blog.csdn.net/stpenghui/article/details/75980032?locationNum=3&fps=1

#saved_filename = 'stock.xlsx'

#df = ts.get_hist_data('002415', start='2018-05-28', end='2018-05-30')

#df.to_excel(saved_filename)


阅读数：147
使用matplotlib和tushare绘制K线与成交量组合图

http://blog.csdn.net/u014281392/article/details/73611624

tushare应用小实例

http://blog.csdn.net/robertsong2004/article/details/50643198

使用tushare获取股票历史行情数据并导入数据库（后复权及未复权）

http://blog.csdn.net/hualugu_6/article/details/54944248?locationNum=1&fps=1

tushare获取数据并存入excel数据表

http://blog.csdn.net/elite666/article/details/62882229?locationNum=1&fps=1

使用tushare开发股票分析脚本

http://blog.csdn.net/stpenghui/article/details/75980032?locationNum=3&fps=1

