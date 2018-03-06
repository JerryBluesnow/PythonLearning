# This is for C HOOK for Game
# [全系统注入-游戏安全实验室](http://gslab.qq.com/article-204-1.html)

# [游戏修改器制作教程七：注入DLL的各种姿势](http://blog.csdn.net/xfgryujk/article/details/50478295)

# [游戏注入教程（一）--远程线程注入](http://blog.csdn.net/wyansai/article/details/52077963)

# [农民工の博客-5篇文章](http://blog.csdn.net/wyansai/article/category/6328876)

# [郁金香外挂技术](http://www.yjxsoft.com/forum.php?mod=forumdisplay&fid=4)

# [外挂制作技术](http://blog.sina.com.cn/s/articlelist_1457737921_0_1.html)

# [[视频]编写代码读取游戏数据-注入DLL](http://www.iqiyi.com/w_19rteanr1h.html)

# [[讨论]绕开游戏对全局钩子的检测](http://bbs.csdn.net/topics/370046194)

# [游戏外挂编程之神器CE的使用 ](http://www.cnblogs.com/egojit/archive/2013/06/14/3135147.html)

# [游戏外挂编程三之游戏进程钩子](https://www.cnblogs.com/egojit/archive/2013/06/16/3138266.html)

# [HOOK钩子的概念](https://jingyan.baidu.com/article/e75aca855afa03142fdac643.html)

# [HOOK钩子教程](http://blog.sina.com.cn/s/blog_651cccf70100tkv6.html)

# [多线程防关,防杀,防删除自身保护程序编写思路](https://www.2cto.com/kf/201002/44758.html)

# [如何让你的程序避开全局键盘钩子的监视](http://blog.okbase.net/BlueSky/archive/3839.html)

# [[CSDN]API HOOK 全局钩子， 防止进程被杀](http://download.csdn.net/download/lygf666/4164019)
# [XueTr这个牛B工具的进程钩子检测如何实现？？](https://bbs.pediy.com/thread-163373.htm)
# [[知乎]Win10下用SetWindowsHookEx设置钩子后部分进程假死？](https://www.zhihu.com/question/64221483)
# [SetWindowsHookEx为某个进程安装钩子](http://blog.csdn.net/hczhiyue/article/details/18449455)
# [HOOK API（四）—— 进程防终止](https://www.cnblogs.com/fanling999/p/4601118.html)
# [PChunter里边有个扫描指定进程中所有钩子的功能，原理是什么？](https://bbs.pediy.com/thread-210688.htm)
# [GOON](http)
# [GOON](http)
# [GOON](http)
# [GOON](http)
# [GOON](http)
# [GOON](http)
# [GOON](http)
# [GOON](http)


# Tips 
## 驱动级注入
    教程:1、打开驱动级别的dll注入器.exe 2、加载驱动 填写要操作的进程名  填写要注入  dll的路径   3 点设置完毕  注意不要关掉
    可以打开要注入的进程测试一下，可注入大部分有保护的游戏
## 游戏应用层钩子
    1. 直接加载驱动的办法过掉钩子，不需要什么XT 
    2. 代码直接注入到游戏进程
    3. 好像很多游戏把钩子什么的都屏蔽了吧，话说我也不怎么懂啊
    @ 春色园
    是的，但是普通游戏是没有屏蔽掉的。即使屏蔽了我们还是有其它办法把我们的代码写入游戏   内存。只要技术够牛连Windows系统内核占据的内存都可以操作，何况运行在windows下的游戏进程内存？？
    4. LPWSTR s1=(LPWSTR)(LPCTSTR)txt_prc_name;
    好丑的代码，建议楼主以后不要用这样的代码了。丑陋不说，还有重大隐患。正确做法是使用   CString::GetBuffer.外挂除了实现功能外最重要是稳定，一些细节你不注意你的外挂就没  市场了。
    说到代码的健壮性，还有你的SetHook 形参没必要用LPWSTR啊，直接LPCWSTR就OK，更好的 是LPCTSTR。
    建议楼主打好扎实的基础知识，走稳了再跑。
    话可能有些不好听，请见谅

