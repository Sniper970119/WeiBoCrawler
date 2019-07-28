# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import pickle
import io
import os

from src import config
import logging

logging.basicConfig(level=config.LOGGING_LEVEL,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

from src.loginWeiBo import GetCookies


class LoginWithCookies(object):
    def __init__(self, executable_path="./driver/win/"):
        try:
            executable_path_1 = executable_path + 'chromedriver.exe'
            # 初始化自动测试驱动
            self.driver = webdriver.Chrome(executable_path=executable_path_1)
        except:
            executable_path_2 = executable_path + 'geckodriver.exe'
            # 初始化自动测试驱动
            self.driver = webdriver.Firefox(executable_path=executable_path_2)
        # 初始化等待时间，10s
        self.wait = WebDriverWait(self.driver, timeout=10)
        pass

    def login_with_cookie(self):
        self.driver.get("https://s.weibo.com/")
        # 把cookie文件加载出来
        with io.open("./cookie/cookies.pkl", "rb") as cookiefile:
            cookies = pickle.load(cookiefile)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        logging.info('load cookies and try to login with cookies')
        self.driver.get('https://s.weibo.com/')
        # 如果cookie没有登录成功，重新获取cookies
        try:
            # 最大化窗口
            self.driver.maximize_window()
            WebDriverWait(self.driver, timeout=10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.gn_name')))
            logging.info('cookies is available')
            return self.driver
        except:
            # cookies失效，删除失效文件重新获取
            logging.info('cookies is not available')
            os.remove('./cookie/cookies.pkl')
            GetCookies.GetCookies()
            self.login_with_cookie()
