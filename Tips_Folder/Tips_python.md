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