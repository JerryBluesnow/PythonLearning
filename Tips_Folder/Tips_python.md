# python的安装

首先，从Python的官方网站 www.python.org下载最新的2.7.6版本，地址是这个：

http://www.python.org/ftp/python/2.7.6/python-2.7.6.msi

然后，运行下载的MSI安装包，不需要更改任何默认设置，直接一路点“Next”即可完成安装：

默认会安装到C:\Python27目录下，但是当你兴致勃勃地打开命令提示符窗口，敲入python后，会得到：

    ‘python’不是内部或外部命令，也不是可运行的程序或批处理文件。

这是因为Windows会根据一个Path的环境变量设定的路径去查找python.exe，如果没找到，就会报错。解决办法是把python.exe所在的路径C:\Python27添加到Path中。

现在，再打开一个新的命令行窗口（一定要关掉原来的命令行窗口，再新开一个），输入python： 

你看到提示符>>>就表示我们已经在Python交互式环境中了，可以输入任何Python代码，回车后会立刻得到执行结果。现在，输入exit()并回车，就可以退出Python交互式环境（直接关掉命令行窗口也可以！）。 

# pip安装
1. 在以下地址下载最新的PIP安装文件：http://pypi.python.org/pypi/pip#downloads
2. 下载pip-7.1.2.tar.gz (md5, pgp)完成之后，解压到一个文件夹，用CMD控制台进入解压目录，输入：
    python setup.py install  

安装好之后，我们直接在命令行输入pip，同样会显示‘pip’不是内部命令，也不是可运行的程序。因为我们还没有添加环境变量。
    C:\Python27\Scripts

# 用pip去安装其他python库
    python -m pip install jieta
    pip install jieta 

# join() function
## 对序列进行操作（分别使用' '与':'作为分隔符）
  
    >>> seq1 = ['hello','good','boy','doiido']
    >>> print ' '.join(seq1)
    hello good boy doiido
    >>> print ':'.join(seq1)
    hello:good:boy:doiido
  
## 对字符串进行操作
  
    >>> seq2 = "hello good boy doiido"
    >>> print ':'.join(seq2)
    h:e:l:l:o: :g:o:o:d: :b:o:y: :d:o:i:i:d:o
   
## 对元组进行操作
  
    >>> seq3 = ('hello','good','boy','doiido')
    >>> print ':'.join(seq3)
    hello:good:boy:doiido
  
## 对字典进行操作
  
    >>> seq4 = {'hello':1,'good':2,'boy':3,'doiido':4}
    >>> print ':'.join(seq4)
    boy:good:doiido:hello
  
## 合并目录
  
    >>> import os
    >>> os.path.join('/hello/','good/boy/','doiido')
    '/hello/good/boy/doiido'

## 如果当前电脑里所有的python程序访问网页或者服务器的时候都需要用到代理可以去python库的源文件修改代理，这样所有用到该源文件访问
    例如我在使用tushare访问数据的时候，实际上默认程序是不走代理的，虽然系统中配置了代理，依然不起任何作用，这个时候发现tushare在访问网页/服务器的时候，
    最终调用的是urlib2.py， 而平时在自己写脚本的时候在脚本中使用build一个新的ProxyHandler就可以了，如下：
    # -*- coding: utf-8 -*-
    import urllib
    import urllib2
    import gzip, StringIO
    import zlib
    
    '''
    proxy_handler = urllib2.ProxyHandler({'http': '135.245.48.34:8000'})
    opener = urllib2.build_opener(proxy_handler)
    r = opener.open('http://finance.sina.com.cn/realstock/company/sz300033/nc.shtml')
    print(r.read())
    '''
    
    request = urllib2.Request('http://www.163.com')
    request.add_header('Accept-encoding', 'gzip')
    
    proxy_handler = urllib2.ProxyHandler({'http': '135.245.48.34:8000'})
    opener = urllib2.build_opener(proxy_handler)
    
    response = opener.open(request)
    html = response.read()
    
    gzipped = response.headers.get('Content-Encoding')
    if gzipped:
        html = StringIO.StringIO(html)
        #html = zlib.decompress(html, 16 + zlib.MAX_WBITS)
        gzipper = gzip.GzipFile(fileobj=html)
        html = gzipper.read()
    else:
        typeEncode = sys.getfilesystemencoding()##系统默认编码
        infoencode = chardet.detect(html).get('encoding','utf-8')##通过第3方模块来自动提取网页的编码
        html = content.decode(infoencode,'ignore').encode(typeEncode)##先转换成unicode编码，然后转换系统编码输出
    
    print html
    
    但是在大量应用中很难做到直接去修改所有的库去build proxyhandler， 所以我们可以采用修改基础库urllib2中的ProxyHandler __init__的constext默认参数设置代理
    class ProxyHandler(BaseHandler):
    ...
    def __init__(self, proxies=None):   
    ----> 
    def __init__(self, proxies={'http': 'xxx.xxx.xxx.xxx:xx'}):    
    其中xxx.xxx.xxx.xxx:xx具体的代理，在浏览器的代理中可以查到.