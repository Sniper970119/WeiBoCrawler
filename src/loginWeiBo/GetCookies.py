# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from tkinter import messagebox

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
        # 查看是否有保存用户cookies，以判断使用哪种方式登录
        if os.path.exists("./cookie/cookies.pkl"):
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
        print('\033[33m--------------需要进行登录，请尽快完成----------------\033[0m')
        print('\033[33m--------------帐号密码登录请在30秒内完成--------------\033[0m')
        print('\033[33m--------------第三方（QQ）登录请在10秒内完成----------\033[0m')

        self.driver.get('https://s.weibo.com/?display=0&retcode=6102#_loginLayer_1562581243968')
        self.driver.maximize_window()
        self.driver.refresh()
        # 获取登录按钮
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.gn_login_list > li:nth-child(3) > a:nth-child(1)')))
        logging.info('login button has been found')
        time.sleep(1)
        login_button.click()
        # 停留10秒，作为用户输入用户名的停留（其实主要是因为要留第三方登录的刷新时间）
        time.sleep(20)
        windows = self.driver.window_handles
        # 如果用户选择了第三方登录，会弹出新的选项卡来登录，那就需要刷新和切换选项卡以寻找标记
        if len(windows) > 1:
            logging.info('user use qq to login')
            # 这里需要对页面进行刷新，对应处理第三方登录的单独弹窗登录
            self.driver.refresh()
            logging.info('refresh page')
            # 切换到第一选项卡
            self.driver.switch_to.window(windows[0])
        # 最大化窗口 寻找登录标记
        self.driver.maximize_window()
        try:
            # 登录检查,这里给最多再给30秒用来进行登录，这里作为输入用户名和密码的等待，第三方登录最多允许10秒
            WebDriverWait(self.driver, timeout=30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.gn_name')))
            logging.info('user has been login')
        except:
            messagebox.showinfo("提示", "登录超时，重新运行")
            exit(0)
        # 获取用户当前cookies
        cookies = self.driver.get_cookies()
        # 将cookies写入文件
        if not os.path.exists("cookie"):
            os.mkdir("cookie")
        pickle.dump(cookies, io.open("./cookie/cookies.pkl", "wb"))
        logging.info('cookies has been saved')
        self.driver.quit()
