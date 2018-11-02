import gzip

import StringIO

import urllib2



ur1='http://www.runoob.com/python/python-exercise-example1.html'

proxy_handler = urllib2.ProxyHandler({'http': 'xxx.xxx.xxx.xxx:xxxx'})
opener = urllib2.build_opener(proxy_handler)

reponse = opener.open(ur1)

r=reponse.read()

data = StringIO.StringIO(r)

gzipper = gzip.GzipFile(fileobj=data)

html = gzipper.read()

print html