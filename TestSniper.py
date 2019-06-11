# -*- coding:utf-8 -*-

if __name__ == '__main__':
    """
    获取cookies测试
    """
    from src.loginWeiBo import GetCookies
    # GetCookies.GetCookies()
    """
    使用cookies登录测试
    """
    from src.systemTools import LoginWithCookies
    # LoginWithCookies.LoginWithCookies()
    """
    寻找抽奖微博测试
    """
    from src.handleAwardWeiBo import FindAwardWeiBo
    FindAwardWeiBo.FindAwardWeiBo().find_one_page()


    pass