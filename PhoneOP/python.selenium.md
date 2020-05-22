+ [python selenium TouchAction模拟移动端触摸操作（十八）](https://www.cnblogs.com/mengyu/p/8136421.html)

+ [python 自动生成useragent/User-Agent方法全解析](https://www.jb51.cc/python/538552.html)

+ [谷歌修改useragent，chrome模拟微信、QQ内置浏览器](https://blog.csdn.net/two_too/article/details/96099019)

+ [利用Chrome在PC电脑上模拟微信内置浏览器](https://blog.csdn.net/xialong_927/article/details/95180583)

+ [selenium+python配置chrome浏览器的选项](https://blog.csdn.net/zwq912318834/article/details/78933910)

+ [查找User-Agent](http://www.fynas.com/ua)

+ [TouchAction实现连续滑动设置手势密码](https://www.cnblogs.com/bendouyao/p/9462788.html)

+ [find_element_by_xpath()的6种方法](https://www.cnblogs.com/liangblog/p/11943877.html)

## 安卓微信内置浏览器 UA:

Mozilla/5.0 (Linux; Android 5.0; SM-N9100 Build/LRX21V) > AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 > Chrome/37.0.0.0 Mobile Safari/537.36 > MicroMessenger/6.0.2.56_r958800.520 NetType/WIFI

## IOS  微信内置浏览器 UA:

Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) > AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 > MicroMessenger/6.0.1 NetType/WIFI

## TouchAction提供的方法：
```
double_tap(on_element)                                                #双击   
flick_element(on_element, xoffset, yoffset, speed)         #从元素开始以指定的速度移动
long_press(on_element)　　                                          #长按不释放
move(xcoord, ycoord)　　                                              #移动到指定的位置
perform()　　                                                                  #执行链中的所有动作
release(xcoord, ycoord)　　                                           #在某个位置松开操作
scroll(xoffset, yoffset)                                                      #滚动到某个位置
scroll_from_element(on_element, xoffset, yoffset)         #从某元素开始滚动到某个位置
tap(on_element)                                                             #单击
tap_and_hold(xcoord, ycoord)                                        #某点按住
```
