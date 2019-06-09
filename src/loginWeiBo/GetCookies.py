# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
import pickle
import io
from src import config
import logging

logging.basicConfig(level=config.LOGGING_LEVEL,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class GetCookies(object):
    """
    执行登录操作
    """

    def __init__(self, executable_path="../driver/win/chromedriver.exe"):
        # 初始化自动测试驱动
        self.driver = webdriver.Chrome(executable_path=executable_path)
        # 初始化等待时间，10s
        self.wait = WebDriverWait(self.driver, timeout=10)
        # 查看是否有保存用户cookies，以判断使用哪种方式登录
        if os.path.exists("../../cookie/cookies.pkl"):
            logging.info('have cookies in file')
        else:
            logging.info('no cookies in file')
            self.login()
        pass

    def login(self):
        """
        登录操作，获取cookies
        :return:
        """
        self.driver.get('https://s.weibo.com')
        # 获取登录按钮
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.gn_login_list > li:nth-child(3) > a:nth-child(1)')))
        logging.info('login button has been found')
        login_button.click()
        # 停留10秒，作为用户输入用户名的停留（其实主要是因为要留第三方登录的刷新时间）
        time.sleep(10)
        # 这里需要对页面进行刷新，对应处理第三方登录的单独弹窗登录
        self.driver.refresh()
        logging.info('refresh page')
        # 登录检查,这里给最多再给30秒用来进行登录，这里作为输入用户名和密码的等待，第三方登录最多允许10秒
        WebDriverWait(self.driver, timeout=30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.gn_name')))
        logging.info('user has been login')
        # 获取用户当前cookies
        cookies = self.driver.get_cookies()
        # 将cookies写入文件
        if not os.path.exists("cookie"):
            os.mkdir("cookie")
        pickle.dump(cookies, io.open("./cookie/cookies.pkl", "wb"))
        logging.info('cookies has been saved')
        self.driver.close()
        print('hello,world')
