import re
import requests
import itchat
import time
from urllib.parse import quote
# 如果上面的itchat库没有安装的话需要先   pip install itchat

# 下面的是从nopwdLogin的body包中抠出来填写的。
jscode = '011Mg6Qm1ZVM5q0VpXOm1dV0Qm1Mg6Qd'
# 上面这个每一个小时更新一次，下面的内容以后可以不更新。。
wx_code = '001khpvq1W4i5k0F6Kwq1PDpvq1khpv9'
wx_header = 'https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJEaibJlVrdF9raOyeEHNsug418YhSuFOaIyKfh3Xt1mUygorZQX31H1HlNgTp0ll8XaozdVmEtveg/132'  # body包中的微信头像wx_header
wx_nickname = '我的网名'  # body包中的微信昵称   wx_header 和wx_nickname其实不是很重要，主要是显示在助力的人列表下面的。
# '上面的定义好后才可以执行代码。。。。。。。。。。。。。。'
# '下面的内容都不要修改。。。。。。。。。。。。。。。。。。'

Cookie1 = {
    'citicbank':'b9ceba79625e35f166de551f88f65dd3',
    'JSESSIONID_BASEH5':'C55196CC00C2E1999B6092933A4BB2FC',
    'JSESSIONID_OAUTH':'C55196CC00C2E1999B6092933A4BB2FC',
    'citicbank_cookie':'!Tr0u1n17blQ6pca7WDSPiZPLSyIDtBu/gPcKbh7ijie8rVbukszjn8XyZbTJ/tJWsffKgk1n6R64ffA',
}

# 下面的不管他。。
itchat.auto_login()

headers ={
    'Accept-Encoding': 'br, gzip, deflate',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=utf-8',
    'Accept': '*/*',
    'Host': 's.creditcard.ecitic.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 MicroMessenger/6.7.4(0x1607042c) NetType/WIFI Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx13b9861d3e9fcdb0/11/page-frame.html',
    'Accept-Language': 'zh-cn',
    'X-Requested-With': 'XMLHttpRequest'
}

@itchat.msg_register([itchat.content.SHARING,itchat.content.TEXT], isGroupChat = True)
def group_reply(msg):
    if 'unionid=' in str(msg):
        searchObj = re.search('unionid=(.*?==)',str(msg))
        if searchObj:
            uid = searchObj.group().replace('unionid=', '')
            ret = enjoy(uid)  # 自动点击助力
            ins(uid)
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), msg.actualNickName, ret)

def enjoy(uid):
    data ='{"code":"%s","encryptedData":"","iv":"JaX/ZnbekWj5kzDitJ9Bow==","channel":"WeChatMini"}' % (jscode)
    r = requests.post('https://uc.creditcard.ecitic.com/citiccard/newucwap/wx/nopwdLogin.do',data=data, headers=headers,timeout=20)
    try:
        authKey = r.json()['authKey']
        Cookie1['JSESSIONID_BASEH5'] = authKey
        Cookie1['JSESSIONID_OAUTH'] = authKey
        tmp = '77777777'
        i = 0
        while '777777' in tmp and i < 4:  # 针对服务拥堵做4次尝试，还得避免死循环
            i += 1
            data = '{"wx_code":"%s","encryptedData":"","iv":"JaX/ZnbekWj5kzDitJ9Bow==","wx_header":"%s","wx_nickname":"%s"}' % (wx_code,wx_header,wx_nickname)
            r = requests.post('https://s.creditcard.ecitic.com/citiccard/gwapi/winterpig/user/login',data=data.encode('utf-8'), headers=headers, cookies=Cookie1,timeout=20)
            tmp = r.text
        unionidSrc = r.json()['unionId']
        citicbank_cookie = r.cookies.get_dict()
        if len(citicbank_cookie) > 0:
            Cookie1['citicbank_cookie'] = r.cookies.get_dict()['citicbank_cookie']
        tmp = '77777777'
        i = 0
        while '777777' in tmp and i < 4:   # 针对服务拥堵做4次尝试，还得避免死循环
            i += 1
            data = '{"unionidDst":"%s","unionidSrc":"%s",' \
                   '"wx_header":"%s","wx_nickname":"%s"}'%(uid,unionidSrc,wx_header,wx_nickname)
            r = requests.post('https://s.creditcard.ecitic.com/citiccard/gwapi/winterpig/assistance/enjoy', data=data.encode('utf-8'), headers=headers, cookies=Cookie1,timeout=20)
            ret = (r.json()['retMsg'])
            tmp = r.text

        if '登录' not in ret:  # 这个及下面2行可以不要，主要是加了可以方便看自己有多少刷子了，不加的话速度能更快些吧
            r = requests.post('https://s.creditcard.ecitic.com/citiccard/gwapi/uc/winterpig/pig/querycurrent', data='{}', headers=headers, cookies=Cookie1,timeout=20)
            ret += '   当前拥有刷子' + str(r.json()['data']['residue'])
        return ret
    except:
        return r.text

def ins(id):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://www.wqh.tw',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15',
        'Referer': 'http://www.wqh.tw/ins.php'
    }
    data = 'fname=' + quote(id, encoding='gbk')
    requests.post('http://wqh.tw/ins.php', data=data, headers=headers)


if __name__ == '__main__':
    itchat.run()
    # print(enjoy('ZtVTjjgITEpXjJz5I00t3A6yxSqgGdgoRNbV4iQEWwS4jprnYL0+uoGac2YV1yPvi3\/scv5hb49w8xP841JmAQ=='))






