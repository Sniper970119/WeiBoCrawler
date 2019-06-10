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

class ForwardWeiBo(object):
    """
    转发微博
    """
