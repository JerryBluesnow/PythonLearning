#!/usr/bin/python
# coding: UTF-8
import requests
import re
import bs4
import traceback

def getHTMLText(url, code = "utf-8"):
    # 获得股票页面
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        # r.encoding = r.apparent_encoding
        # 直接用"utf-8"编码节省时间
        return r.text
    except:
        return ""

def getStockList(lst, stockURL):
    # 获取股票列表
    html = getHTMLText(stockURL, "GB2312")
    # 东方财富网用"GB2312"方式编码
    soup = bs4.BeautifulSoup(html, "html.parser")
    a = soup. find_all("a")
    for i in a:
        try:
            href = i.attrs["href"]
            lst.append(re.findall(r"[s][hz]\d{6}", href)[0])
        except:
            continue

def getStockInfo(lst, stockURL, fpath):

    count = 0
    # 增加进度条

    # 获取个股信息
    for stock in lst:
        url = stockURL + stock + ".html"
        html = getHTMLText(url)
        try:
            if html == "":
            # 判断页面是否为空
                continue
            infoDict = { }
            # 定义一个字典用来储存股票信息
            soup = bs4.BeautifulSoup(html, "html.parser")
            stockInfo = soup.find("div", attrs={"class":"stock-bets"})
            # 获得股票信息标签

            name = stockInfo.find_all(attrs={"class":"bets-name"})[0]
            # 在标签中查找股票名称
            infoDict.update({"股票名称":name.text.split()[0]})
            # 将股票名称增加到字典中

            keyList = stockInfo.find_all("dt")
            # "dt"标签是股票信息键的域
            valueList = stockInfo.find_all("dd")
            # "dd"标签是股票信息值的域

            for i in range(len(keyList)):
            # 还原键值对并存储到列表中
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val

            with open(fpath, "a", encoding="utf-8") as f:
                f.write(str(infoDict) + "\n")

                count += 1
                # 增加进度条
                print "\rcurrent process:%.2f" % (count*100/len(lst))

        except:
            count += 1
            # 增加进度条
            print 'current process:%.2f' % (count * 100 / len(lst))

            # 用traceback获得异常信息
            #traceback.print_exc()
            continue
    return ""

if __name__ == '__main__':
    stock_list_url = "http://quote.eastmoney.com/stocklist.html"
    # 获得个股链接
    stock_info_url = "https://gupiao.baidu.com/stock/"
    # 获取股票信息的主题部分
    output_file = "C:\\Users\\W419L\\Desktop\\股票爬取.txt"
    # 文件保存地址
    slist = []
    # 存储股票信息
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)