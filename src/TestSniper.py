# -*- coding:utf-8 -*-
from src.loginWeiBo import GetCookies
from src.systemTools import LoginWithCookies
from src.handleAwardWeiBo import FindAwardWeiBo

if __name__ == '__main__':
    """
    获取cookies测试
    """
    GetCookies.GetCookies()
    """
    使用cookies登录测试
    """
    LoginWithCookies.LoginWithCookies()
    """
    寻找抽奖微博测试
    """
    # FindAwardWeiBo.FindAwardWeiBo()

    pass