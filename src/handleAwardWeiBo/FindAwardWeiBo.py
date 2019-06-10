# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from src.systemTools import LoginWithCookies
import urllib.parse
import time
import re

from src.handleAwardWeiBo import FindCondation


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
        # 生成bs4对象
        soup = BeautifulSoup(text, 'html5lib')
        # 将该页微博的微博id正则出
        weibo_list = re.findall('.*?feed_list_item" mid="(.*?)">', str(text))
        # 使用bs4 获取微博的正文（为什么不用正则呢，因为正则如果加上re.S 慢的我想死）
        get_info = soup.find_all('p', attrs={'node-type': 'feed_list_content'})
        weibo_main_body = []
        for i in get_info:
            weibo_main_body.append(str(i))
        condation = FindCondation.FindCondation().find_condation(weibo_list, weibo_main_body)
        # 处理当前页的微博
        for i in range(1, len(weibo_list) + 1):
            weibo_id = 1
        pass

# pl_feedlist_index > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1)
# pl_feedlist_index > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1)
