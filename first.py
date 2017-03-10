import urllib2

r = urllib2.Request("http://classweb.loxa.com.tw/dino123/air/P1000775.jpg")

try:
    # print 111111111111111111
    #f = urllib2.urlopen(r, data=None, timeout=3)
    # print 2222222222222222
    # result =  f.read()
    print 333333333333333333
except Exception, e:
    print "444444444444444444---------" + str(e)

import time

localtime = time.asctime(time.localtime(time.time()))
print "current local time is :", localtime

import calendar
cal = calendar.month(2017, 3)
print cal


def powerpower(x, y=2):
    sum = 1
    while y > 0:
        y = y - 1
        sum = sum * x
    return sum

def powerpower2(x, y, z):
    return x * y * z

print powerpower(10, 4) + powerpower2(10, 20, 31) + powerpower(20)

def enrollstudent(name, sex, age=6, city="QD"):
    print 'name', name.ljust(10), 'sex', sex.ljust(10), 'age', age, 'city', city.ljust(10)

enrollstudent("Jerryzhang", "male", city="BeiJing")
enrollstudent("MerryH", "female", age=7, city="Shanghai")


def add_end(LIST=None):
    if LIST is None:
        LIST = []
    LIST.append('END')
    return LIST

print add_end()
print add_end(['THIG'])

def calc(numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum


print calc([1, 2, 3])

def calc2(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum

print calc2(1, 2, 3)

def person(name, age, **keyword):
    if 'city' in keyword:
        pass
    if 'job' in keyword:
        pass
    print 'name', name.ljust(10), 'age', age, 'other', keyword

person('HengHeng', 1.6, city='Beijing', addr='Chaoyang', zipcode=123456)
