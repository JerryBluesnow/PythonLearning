[Git教程--廖雪峰](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)

# get change from remote 相当于是从远程获取最新版本到本地，不会自动merge
git fetch origin master  
git log -p master..origin/master  
git merge origin/master  

# get change from remote 相当于是从远程获取最新版本并merge到本地
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
### git config查看配置 
    git config --list

## git删除文件
    local operation steps:
    rm file_name
    git status
    git rm file_name
    git status
    git commit -m "remove file_name"
    git push origin master

## check out 单个文件
    git checkout -- reademe.txt
## [撤销修改也可以checkout，也可以reset HEAD](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/001374831943254ee90db11b13d4ba9a73b9047f4fb968d000)
