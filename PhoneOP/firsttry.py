# -*- coding: utf-8 -*-
# @Time    : 2017/12/28 10:26
# @Author  : Hunk
# @File    : ex86.py.py
# @Software: PyCharm
import time
from selenium import webdriver
from selenium.webdriver.common.touch_actions import TouchActions
 
"""设置手机的大小"""
mobileEmulation = {'deviceName': 'iPhone 5/SE'}
options = webdriver.ChromeOptions()
options.add_experimental_option('mobileEmulation', mobileEmulation)

'''设置编码格式'''
options.add_argument('lang=zh_CN.UTF-8')

'''模拟iphone 6'''
options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')

'''禁止加载图片'''
#prefs = {"profile.managed_default_content_settings.images": 2}
#options.add_experimental_option("prefs", prefs)

'''Cannot call non W3C standard command while in W3C mode问题解决'''
options.add_experimental_option('w3c', False)

driver = webdriver.Chrome(chrome_options=options)
driver.get('http://www.jrdxdnx.cn/')
driver.maximize_window()
"""定位操作元素"""
#button = driver.find_element_by_xpath('//*[@id="kw"]')
Action = TouchActions(driver)
"""从button元素像下滑动200元素，以50的速度向下滑动"""
#Action.flick_element(button, 0, 200, 50).perform()
#Action.scroll_from_element(button, 0, -200).perform()
Action.scroll(0, 400).perform()
time.sleep(3)
driver.close()