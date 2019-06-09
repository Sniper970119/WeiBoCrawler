# -*- coding:utf-8 -*-
from selenium.webdriver.support.wait import WebDriverWait
from src.systemTools import LoginWithCookies
import urllib.parse
import time


class FindAwardWeiBo(object):
    def __init__(self):
        # 初始化已经带cookies的测试驱动
        self.driver = LoginWithCookies.LoginWithCookies().login_with_cookie()
        # 初始化等待时间，10s
        self.wait = WebDriverWait(self.driver, timeout=10)
        pass

    def find_one_page(self, pagenumber=1):
        # 关键字编码
        keyword_change = urllib.parse.quote_plus('抽奖')
        keyword_change = urllib.parse.quote_plus(keyword_change)
        # 构建URL
        url = 'https://s.weibo.com/weibo/' + keyword_change + '&xsort=hot&page=%s' % (str(pagenumber))
        self.driver.get(url)
        text = self.driver.page_source
        pass
