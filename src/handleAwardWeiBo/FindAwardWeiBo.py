# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from src.loginWeiBo import GetCookies
from src.systemTools import LoginWithCookies
from src.systemTools import HandleUserInDatabase
import urllib.parse
import time
import re
import configparser

from src import config
import logging

logging.basicConfig(level=config.LOGGING_LEVEL,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

from src.handleAwardWeiBo import FindCondation


class FindAwardWeiBo(object):
    def __init__(self):
        # 读取配置文件，获得两个朋友微博id，用来处理有的微博需要at两个好友
        cf = configparser.ConfigParser()
        cf.read('./friends.ini', encoding='utf-8')
        self.friend_1 = cf.get('FRIENDS', 'friend_1')
        self.friend_2 = cf.get('FRIENDS', 'friend_2')
        GetCookies.GetCookies()
        self.user_database_tools = HandleUserInDatabase.HandleUserInDatabase()
        pass

    def find_one_page(self, pagenumber=1):
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
        text = self.driver.page_source
        # 生成bs4对象
        soup = BeautifulSoup(text, 'html5lib')
        # 将该页微博的微博id正则出
        weibo_list = re.findall('.*?feed_list_item" mid="(.*?)">', str(text))
        # 使用bs4 获取微博的正文（为什么不用正则呢，因为正则如果加上re.S 慢的我想死）
        get_info = soup.find_all('p', attrs={'node-type': 'feed_list_content'})
        weibo_main_body = []
        for i in get_info:
            weibo_main_body.append(str(i))
        # 获取当前页微博简单处理后的抽奖要求
        condation = FindCondation.FindCondation().find_condation(weibo_list, weibo_main_body)
        # 处理当前页的微博
        for i in range(0, len(weibo_list)):
            forword = False
            index_id = i + 1
            print(index_id)
            # 处理点赞
            if condation[i]['need_zan'] == '1':
                # 关注, 只执行（判断）一次
                if forword is False:
                    self.attention_user(index_id)
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
            if condation[i]['need_attention'] == '1':
                # 关注, 只执行一次
                if forword is False:
                    self.attention_user(index_id)
                    forword = True

            # 处理转发
            if condation[i]['need_forward'] == '1':
                # 关注, 只执行一次
                if forword is False:
                    self.attention_user(index_id)
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
                forward_text = '1234'
                # 如果需要at好友
                if condation[i]['need_at_friend'] == '1':
                    forward_text = '@' + self.friend_1 + '  @' + self.friend_2
                forward_input_text.send_keys(forward_text)
                # 获取转发按钮
                forward_input_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR,
                         '.s-btn-g')))
                logging.info('forward input button has been found')
                forward_input_button.click()
            pass
        self.driver.quit()
        pass

    def attention_user(self, index_id):
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
        avatar_button.click()
        # 切换到新页面
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[1])
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
        self.user_database_tools.save_data(uid)
        # 切换回搜索页面
        self.driver.switch_to.window(windows[0])
        pass

# pl_feedlist_index > div:nth-child(2) > div:nth-child(1) > div > div.card-act > ul > li:nth-child(4) > a
# pl_feedlist_index > div:nth-child(2) > div:nth-child(2) > div > div.card-act > ul > li:nth-child(4) > a
