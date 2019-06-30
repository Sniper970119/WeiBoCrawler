# -*- coding:utf-8 -*-
import random
import threading
import time

from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from src.loginWeiBo import GetCookies
from src.systemTools import LoginWithCookies, HandleWeiBoInDatebase
from src.systemTools import HandleUserInDatabase
from src.handleAwardWeiBo import FindCondation

import urllib.parse
import re
import configparser

from src import config
import logging

logging.basicConfig(level=config.LOGGING_LEVEL,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class FindQianGe(threading.Thread):
    """
    对@钱哥 进行定制化转发
    """

    def __init__(self, *args, **kwargs):
        # 对线程初始化
        super(FindQianGe, self).__init__(*args, **kwargs)
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
        # 钱哥微博地址
        self.url = 'https://weibo.com/u/6074930760?topnav=1&wvr=6&topsug=1&is_all=1'

    def find_weibo(self, url='https://weibo.com/u/6074930760?topnav=1&wvr=6&topsug=1&is_all=1'):
        """
        搜索微博
        :return:
        """
        # 初始化已经带cookies的测试驱动
        self.driver = LoginWithCookies.LoginWithCookies().login_with_cookie()
        # 初始化等待时间，10s
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.driver.get(self.url)
        # 停留2秒作为页面刷新时间
        time.sleep(2)
        text = self.driver.page_source
        # 获取微博用户名
        weibo_user = re.findall("CONFIG.*?onick.*?='(.*?)'", text)[0]
        # 生成bs4对象
        soup = BeautifulSoup(text, 'html5lib')
        # 所有的微博信息
        get_weibo = soup.find_all('div', attrs={'class': 'WB_detail'})
        # 保存微博所有信息的str
        get_weibo_str = []
        # 将该页微博的微博id(mid)正则出
        weibo_mid = []
        # 被转发微博者的昵称
        forwarded_user = []
        # 当前微博正文
        weibo_context = []
        # 被转发的微博正文
        weibo_forwarded_context = []
        for each in get_weibo:
            # 该条微博的全部html代码
            sub_text = str(each)
            # 添加str
            get_weibo_str.append(sub_text)
            # 处理mid
            weibo_mid.append(re.findall('name="(.*?)"', sub_text)[0])
            # 处理被转发微博源用户
            if_forward = re.findall('node-type="feed_list_originNick".*?>(.*?)</a>', sub_text)
            # 处理微博正文
            soup1 = BeautifulSoup(sub_text, 'html5lib')
            # 当前微博正文
            weibo_context.append(
                str(soup1.find_all('div', attrs={'node-type': 'feed_list_content'})[0]).replace(' ', ''))
            # 分情况添加（是否为转发的微博）
            if len(if_forward) > 0:
                forwarded_user.append(if_forward[0])
                # 被转发微博正文
                weibo_forwarded_context.append(
                    str(soup1.find_all('div', attrs={'node-type': 'feed_list_reason'})[0]).replace(' ', ''))
            else:
                forwarded_user.append('')
                weibo_forwarded_context.append('')
        # 处理当前微博的抽奖条件
        current_condation = FindCondation.FindCondation().find_condation(weibo_mid, weibo_context)
        forwarded_condation = FindCondation.FindCondation().find_condation(weibo_mid, weibo_forwarded_context)
        # 遍历每个微博
        for i in range(0, len(weibo_mid)):
            index_id = i + 1
            sub_text = str(get_weibo[i])
            # 判断是否为转发的微博
            origin_user = re.findall('node-type="feed_list_originNick".*?>(.*?)</a>', sub_text)
            if len(origin_user) > 0:
                # 寻找被转发者
                forward_user = re.findall('title="(.*?)"', origin_user[0])
                # 判断被转发者是不是自己
                if forward_user is origin_user:
                    continue
                else:
                    need_ignore = False
                    # 判断该微博是否被操作过，如果没有，执行操作并保存数据库，如果操作过，放弃此趟
                    if current_condation[i]['need_zan'] == '1' or current_condation[i]['need_attention'] == '1' or current_condation[i][
                        'need_forward'] == '1':
                        # 判断是否被操作
                        if HandleWeiBoInDatebase.HandleUserInDatabase().if_have_data_and_save_it(weibo_list[i]):
                            continue
                        pass
                    else:
                        continue
                    # 处理点赞
                    if current_condation[i]['need_zan'] == '1':
                        # 获取点赞按钮,
                        css_like = '#pl_feedlist_index > div:nth-child(2) > div:nth-child(' + str(
                            index_id) + ') > div > div.card-act > ul > li:nth-child(4) > a'
                        like_button = self.wait.until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, css_like)))
                        logging.info('like button has been found')
                        like_button.click()

                    # 处理关注
                    if current_condation[i]['need_attention'] == '1':
                        pass

                    # 处理转发
                    if current_condation[i]['need_forward'] == '1':
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
                        if current_condation[i]['need_at_friend'] == '1':
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
                    if len(current_condation[i]['attention_list']) > 0:
                        for each in current_condation[i]['attention_list']:
                            self.attention_other_user(each)
                        pass
                    # 随机暂停1~n秒
                    time.sleep(random.randint(1, 5))
                    pass
                self.driver.quit()
        pass

    def handle_other_origin(self):
        """
        处理转发他人微博的关注以及点赞等操作
        :return:
        """
        pass

    def attention_other_user(self, user_name):
        """
        关注其他博主
        :param user_name:
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
        text = driver.page_source
        soup = BeautifulSoup(text, 'html5lib')
        # 使用bs4 获取uid附近的字符
        uid_info = soup.find_all('div', attrs={'node-type': 'focusLink'})
        # 获取关注用户的uid
        uid = re.findall("uid=(.*?)&", str(uid_info))[0]
        name = re.findall("fnick=(.*?)&", str(uid_info))[0]
        self.user_database_tools.save_data(uid, name)
        driver.quit()
