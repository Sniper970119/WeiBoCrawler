# -*- coding:utf-8 -*-
from selenium.webdriver.support.wait import WebDriverWait
from src.systemTools import LoginWithCookies
import time


class FindAwardWeiBo(object):
    def __init__(self):
        # 初始化已经带cookies的测试驱动
        self.driver = LoginWithCookies.LoginWithCookies().login_with_cookie()
        # 初始化等待时间，10s
        self.wait = WebDriverWait(self.driver, timeout=10)
        pass

    def find_one_page(self, session, new_cookies, pagenumber=1):
        pass