# -*- coding:utf-8 -*-
import random
import threading
from tkinter import messagebox

from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from src.loginWeiBo import GetCookies
from src.systemTools import LoginWithCookies
from src.systemTools import HandleUserInDatabase
from src.systemTools import HandleWeiBoInDatabase
from src.handleAwardWeiBo.tools import FindCondation
from src.handleAwardWeiBo import StartAutoFind

import urllib.parse
import time
import re
import configparser

from src import config
import logging

logging.basicConfig(level=config.LOGGING_LEVEL,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class FindAwardWeiBo(threading.Thread):
    """
    常规搜索查找
    """

    def __init__(self, *args, **kwargs):
        # 对线程初始化
        super(FindAwardWeiBo, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True
        # 读取配置文件，获得两个朋友微博id，用来处理有的微博需要at两个好友
        cf = configparser.ConfigParser()
        cf.read('./friends.ini', encoding='utf-8')
        self.friend_1 = cf.get('FRIENDS', 'friend_1')
        self.friend_2 = cf.get('FRIENDS', 'friend_2')
        GetCookies.GetCookies()
        self.user_database_tools = HandleUserInDatabase.HandleUserInDatabase()
        pass

    def find_one_page(self, pagenumber=1, from_index=0):
        # 初始化已经带cookies的测试驱动
        self.driver = LoginWithCookies.LoginWithCookies().login_with_cookie()
        # 初始化等待时间，10s
        self.wait = WebDriverWait(self.driver, timeout=10)
        # 关键字编码
        keyword_change = urllib.parse.quote_plus('抽奖')
        keyword_change = urllib.parse.quote_plus(keyword_change)
        # 构建URL
        url = 'https://s.weibo.com/weibo/' + keyword_change + '&xsort=hot&page=%s' % (str(pagenumber))
        self.driver.get(url)
        try:
            self.driver.get(url)
        except:
            messagebox.showinfo("提示", "登录超时，重新运行")
            exit(0)
        text = self.driver.page_source
        # 生成bs4对象
        soup = BeautifulSoup(text, 'html5lib')
        # 将该页微博的微博id(mid)正则出
        weibo_list = re.findall('.*?feed_list_item" mid="(.*?)">', str(text))
        # 使用bs4 获取微博的正文（为什么不用正则呢，因为正则如果加上re.S 慢的我想死）
        get_info = soup.find_all('p', attrs={'node-type': 'feed_list_content'})
        weibo_main_body = []
        for i in get_info:
            weibo_main_body.append(str(i))
        # 获取当前页微博简单处理后的抽奖要求
        condition = FindCondation.FindCondation().find_condation(weibo_list, weibo_main_body)
        # 处理当前页的微博
        for i in range(from_index, len(weibo_list)):
            forword = False
            index_id = i + 1
            print('\033[32m-------------当前处理第' + str(pagenumber) + '页的第' + str(i + 1) + '条微博---------------\033[0m')
            print('\033[32m------------- 点赞：'+str(condition[i]['need_zan'])+' 关注：'+str(condition[i]['need_attention'])+' 转发：'+str(condition[i]['need_forward'])+'---------------\033[0m')
            # 判断该微博是否被操作过，如果没有，执行操作并保存数据库，如果操作过，放弃此趟
            if condition[i]['need_zan'] == '1' or condition[i]['need_attention'] == '1' or condition[i][
                'need_forward'] == '1':
                # 判断是否被操作
                if HandleWeiBoInDatabase.HandleWeiboInDatabase().if_have_data_and_save_it(weibo_list[i]):
                    print('\033[32m---------------已经操作过该条微博-------------------\033[0m')
                    print()
                    continue
                pass
            else:
                print('\033[32m---------------该条微博不需要被操作-------------------\033[0m')
                print()
                continue
            # 处理点赞
            if condition[i]['need_zan'] == '1':
                # 关注, 只执行（判断）一次
                if forword is False:
                    self.attention_user(index_id, pagenumber)
                    forword = True
                # 获取点赞按钮,
                css_like = '#pl_feedlist_index > div:nth-child(2) > div:nth-child(' + str(
                    index_id) + ') > div > div.card-act > ul > li:nth-child(4) > a'
                like_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, css_like)))
                logging.info('like button has been found')
                like_button.click()

            # 处理关注
            if condition[i]['need_attention'] == '1':
                # 关注, 只执行一次
                if forword is False:
                    self.attention_user(index_id, pagenumber)
                    forword = True

            # 处理转发
            if condition[i]['need_forward'] == '1':
                # 关注, 只执行一次
                if forword is False:
                    self.attention_user(index_id, pagenumber)
                    forword = True
                # 获取转发按钮,
                css_forward = '#pl_feedlist_index > div:nth-child(2) > div:nth-child(' + str(
                    index_id) + ') > div:nth-child(1) > div:nth-child(2) > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1)'

                forward_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, css_forward)))
                logging.info('forward button has been found')
                forward_button.click()
                # 获取转发输入
                forward_input_text = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR,
                         'body > div.m-layer > div.inner > div > div:nth-child(2) > div > div.func > div > div.input > textarea')))
                logging.info('forward input text has been found')
                # 随机转发文本
                forward_text = ''.join(random.sample('0123456789', 6))
                # 如果需要at好友
                if condition[i]['need_at_friend'] == '1':
                    forward_text = '@' + self.friend_1 + '  @' + self.friend_2 + '    ' + forward_text
                forward_input_text.send_keys(forward_text)
                # 获取转发按钮
                forward_input_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR,
                         '.s-btn-g')))
                logging.info('forward input button has been found')
                forward_input_button.click()
                time.sleep(random.randint(1, 3))

            # 处理转发微博中的其他关注
            if len(condition[i]['attention_list']) > 0:
                for each in condition[i]['attention_list']:
                    self.attention_other_user(each)
                pass
            # 将该微博保存到数据库
            # HandleWeiBoInDatebase.HandleUserInDatabase().save_data(weibo_list[i])
            # 随机暂停1~n秒
            print('\033[31m----------------成功操作该条微博--------------------\033[0m')
            print()
            time.sleep(random.randint(3, 5))
            pass
        self.driver.quit()
        pass

    def attention_user(self, index_id, page_number):
        """
        关注在当前页下的某博主
        :param index_id: 当前页相对索引id
        :return:
        """
        # 首先获取昵称（用来点击到详情页）
        avatar_css = '#pl_feedlist_index > div:nth-child(2) > div:nth-child(' + str(
            index_id) + ') > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)'
        avatar_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, avatar_css)))
        logging.info('avatar button has been found')
        try:
            avatar_button.click()
        except:
            # 多半是因为上一步转发失败，导致这一步发生错误，开启新线程重新调用方法
            # index -2 是因为所以比i大1，并且上一个失败，所以需要 -1 -1 重新执行操作
            threading.Thread(target=self.award_run, args=(page_number, index_id - 2)).start()
            logging.info('create new threading')
            self.driver.quit()
            logging.info('old thread alive')
            pass
        time.sleep(random.randint(1, 3))
        # 切换到新页面
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        # 查找关注按钮
        attention_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div.btn_bed:nth-child(1) > a:nth-child(1)')))
        logging.info('attention button has been found')
        attention_button.click()
        text = self.driver.page_source
        soup = BeautifulSoup(text, 'html5lib')
        # 使用bs4 获取uid附近的字符
        uid_info = soup.find_all('div', attrs={'node-type': 'focusLink'})
        # 获取关注用户的uid
        uid = re.findall("uid=(.*?)&", str(uid_info))[0]
        name = re.findall("fnick=(.*?)&", str(uid_info))[0]
        self.user_database_tools.save_data(uid, name)
        # 切换回搜索页面
        self.driver.switch_to.window(windows[0])
        time.sleep(random.randint(1, 3))
        pass

    def attention_other_user(self, user_name):
        """
        关注其他用户
        :return:
        """
        # 初始化username
        user_name = '@' + user_name
        # 初始化已经带cookies的测试驱动
        driver = LoginWithCookies.LoginWithCookies().login_with_cookie()
        # 初始化等待时间，10s
        wait = WebDriverWait(driver, timeout=10)
        # 关键字编码
        keyword_change = urllib.parse.quote_plus('抽奖')
        keyword_change = urllib.parse.quote_plus(keyword_change)
        # 构建URL
        url = 'https://s.weibo.com/weibo/' + user_name
        driver.get(url)

        # 找人按钮
        find_people = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'body > div.m-main > div.m-main-nav.s-mt28 > ul > li:nth-child(2) > a')))
        logging.info('find people button has been found')
        find_people.click()
        time.sleep(1)
        # 第一个用户
        user_name_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 '#pl_user_feedList > div:nth-child(1) > div.info > div > a.name')))
        logging.info('user name button has been found')
        user_name_button.click()

        # 切换到新页面
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        # 查找关注按钮
        attention_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 '#Pl_Official_Headerv6__1 > div.PCD_header > div > div.shadow > div.pf_opt > div > div:nth-child(1) > a:nth-child(1)')))
        logging.info('attention button has been found')
        attention_button.click()
        time.sleep(1)
        text = driver.page_source
        soup = BeautifulSoup(text, 'html5lib')
        # 使用bs4 获取uid附近的字符
        uid_info = soup.find_all('div', attrs={'node-type': 'focusLink'})
        # 获取关注用户的uid
        uid = re.findall("uid=(.*?)&", str(uid_info))[0]
        name = re.findall("fnick=(.*?)&", str(uid_info))[0]
        self.user_database_tools.save_data(uid, name)
        driver.quit()

    def award_run(self, from_page=1, index_number=0):
        """
        运行程序
        :return:
        """
        for i in range(from_page, 5):
            print('\033[33m--------------------开始搜索第'+str(i)+'页--------------------\033[0m')
            self.find_one_page(i, index_number)
