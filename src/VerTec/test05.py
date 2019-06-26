# -*- coding:utf-8 -*-
import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait

from src.loginWeiBo import GetCookies
from src.systemTools import LoginWithCookies
from src.systemTools import HandleUserInDatabase


class Test05(object):
    def __init__(self):
        url = 'https://weibo.com/u/6074930760?topnav=1&wvr=6&topsug=1&is_all=1'
        GetCookies.GetCookies()
        user_database_tools = HandleUserInDatabase.HandleUserInDatabase()
        driver = LoginWithCookies.LoginWithCookies().login_with_cookie()
        # 初始化等待时间，10s
        wait = WebDriverWait(driver, timeout=10)

        driver.get(url)
        time.sleep(2)
        text = driver.page_source
        weibo_user = re.findall("CONFIG.*?onick.*?='(.*?)'", text)[0]

        # soup = BeautifulSoup(text, 'html5lib')
        # get_info = soup.find_all('a', attrs={'node-type': 'feed_list_originNick'})
        # for i in get_info:
        #     print(str(i))
        print()
