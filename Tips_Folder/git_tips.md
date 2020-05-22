[Git教程--廖雪峰](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)

## get change from remote 相当于是从远程获取最新版本到本地，不会自动merge
    git fetch origin master  
    git log -p master..origin/master  
    git merge origin/master  

## get change from remote 相当于是从远程获取最新版本并merge到本地
    git pull origin master

    git add filename filename2 file...
    git commit file1 -m "tips"
    git commit -m "tips for all"
    git push origin master
##  [git设置用户名密码](http://blog.csdn.net/qq_15437667/article/details/51029757)
    git config --global user.name [username]
    git config --global user.email [email]
    modify .git/config：
    echo "[credential]" >> .git/config
    echo "    helper = store" >> .git/config
   or [git设置用户/密码](http://blog.csdn.net/qq_28602957/article/details/52154384)
### git config查看配置 
    git config --list
    http.proxy=http://xxx.xxx.xxx.xxx:xxxx
## git删除文件
    local operation steps:
    rm file_name
    git status
    git rm file_name
    git status
    git commit -m "remove file_name"
    git push origin master

## 多个账号同时使用时，要需要设置的全局用户名和用户邮箱，在每个repo目录下单独设置
### 取消全局设置
    git config --global --unset user.name   //取消全局设置
    git config --global --unset user.email  //取消全局设置

### 单独设置
    git config user.name "newname"
    git config user.email "newemail"

## check out 单个文件
    git checkout -- reademe.txt
## 更新单个文件
    $ git fetch
    remote: Counting objects: 8, done.
    remote: Compressing objects: 100% (3/3), done.
    remote: Total 8 (delta 3), reused 8 (delta 3), pack-reused 0
    Unpacking objects: 100% (8/8), done.
    From github.com:fffy2366/checkout
       cd1768d..2408ca5  master     -> origin/master

    $ git checkout -m 2408ca5 1.php 2.php
## 更新单个目录
    $ git fetch

    remote: Counting objects: 8, done.
    remote: Compressing objects: 100% (3/3), done.
    remote: Total 8 (delta 3), reused 8 (delta 3), pack-reused 0
    Unpacking objects: 100% (8/8), done.
    From github.com:fffy2366/checkout
       cd1768d..2408ca5  master     -> origin/master

    $ git checkout -m 2408ca5 test1
### [撤销修改也可以checkout，也可以reset HEAD](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/001374831943254ee90db11b13d4ba9a73b9047f4fb968d000)

## [github/gerrit 管理多个ssh key](http://blog.csdn.net/system1024/article/details/52044900)

## git tips for work

# .gitignore忽略，过滤
 [Git忽略规则.gitignore梳理](https://www.cnblogs.com/kevingrace/p/5690241.html)

 [git 已提交文件的 如何屏蔽git的track](http://blog.csdn.net/n517052183/article/details/45028293)
 正确的做法应该是：git rm --cached logs/xx.log，
 然后更新 .gitignore 忽略掉目标文件，
 最后 git commit -m "We really don't want Git to track this anymore!"

 # git rebase --continue / --skip
 
git rebase --abort 是无风险的操作，会回到rebase操作之前的状态，2个分支的commits毫发无损。
git rebase --skip 是高风险的操作，引起冲突的commits会被丢弃（这部分代码修改会丢失）


# git rm 如何删除中文文件?
    例如手动删除一个中文文件后，执行git status，会得到如下信息
          deleted:    "stock/stock2/stock/\350\202\241\347\245\250\347\273\237\350\256\241.xlsx"
    其实这是一个中文名的文件，执行git rm  "stock/stock2/stock/\350\202\241\347\245\250\347\273\237\350\256\241.xlsx"
    会失败，
    这个时候需要执行如下命令
    git config --global core.quotepath false
    然后,执行git status，会得到中文名：
    deleted:    stock/stock2/stock/股票统计.xlsx
    之后执行git rm stock/stock2/stock/股票统计.xlsx就可以了



jzhan107@lsslinux01.ih.lucent.com:/home_nbu/jzhan107/gitProject/sbc/ssp/ds/ims/ibcf>n$ git remote -v
origin  https://gerrit.ext.net.nokia.com/gerrit/ENT/sbc (fetch)
origin  https://gerrit.ext.net.nokia.com/gerrit/ENT/sbc (push


git commit -m "SBC-1110: this the second change to IBCF_prov_data.cpp to add file comments"




# amend 只能修改最近一次的commit 的comments
git commit --amend 


# 如果有commit没有加SBC-XXXXX
git log # find commit id

commit 9868180908cb0dcc485f75abd87987135002e0b7
Author: jzhan107 <jerry.2.zhang@nokia-sbell.com>
Date:   Wed Aug 28 21:26:46 2019 -0500

    add comments to IBCF_prov_data.cpp

    Change-Id: I165efc1eea2eb52eef139a9edd590682051fd20c

# move commit to the head	
git reset --soft 9868180908cb0dcc485f75abd87987135002e0b7  

# fix the comments
git commit --amend

# still need to push to remote
git push origin HEAD:refs/for/current_learning


今天执行git pull时，碰到如下提示：

First, rewinding head to replay your work on top of it...

参考链接：https://stackoverflow.com/questions/22320058/git-first-rewinding-head-to-replay

看到如下答案：

git fetch origin; git reset --hard origin/<branch>
 ———————————————— 
版权声明：本文为CSDN博主「从心所愿」的原创文章，遵循CC 4.0 by-sa版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/sanbingyutuoniao123/article/details/78187229
