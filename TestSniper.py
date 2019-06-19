# -*- coding:utf-8 -*-
import threading

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

    # FindAwardWeiBo.FindAwardWeiBo().start()
    threading.Thread(target=FindAwardWeiBo.FindAwardWeiBo().find_one_page, args=(1, 0)).start()
    """
    测试关注其他用户
    """
    # FindAwardWeiBo.FindAwardWeiBo().attention_other_user('博物小馆')

pass
