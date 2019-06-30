# -*- coding:utf-8 -*-
import threading

if __name__ == '__main__':
    """
    获取cookies测试
    """

    # GetCookies.GetCookies()
    """
    使用cookies登录测试
    """

    # LoginWithCookies.LoginWithCookies()
    """
    寻找抽奖微博测试
    """
    from src.handleAwardWeiBo.generalFind import FindAwardWeiBo

    # FindAwardWeiBo.FindAwardWeiBo().start()
    # threading.Thread(target=FindAwardWeiBo.FindAwardWeiBo().award_run).start()
    """
    测试关注其他用户
    """
    # FindAwardWeiBo.FindAwardWeiBo().attention_other_user('博物小馆')


    """
    测试单独用户的查找转发
    """
    from src.handleAwardWeiBo.customFind import FindQianGe

    threading.Thread(target=FindQianGe.FindQianGe().find_weibo()).start()


    """
    技术验证根目的测试
    """
    # from src.VerTec import test05
    # test05.Test05()

pass
