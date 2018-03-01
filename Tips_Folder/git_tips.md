# get change from remote 相当于是从远程获取最新版本到本地，不会自动merge
git fetch origin master  
git log -p master..origin/master  
git merge origin/master  

# get change from remote 相当于是从远程获取最新版本并merge到本地
git pull origin master

#

    git add filename filename2 file...
    git commit file1 -m "tips"
    git commit -m "tips for all"
    git push origin master