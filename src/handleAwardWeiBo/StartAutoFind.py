# -*- coding:utf-8 -*-
import threading
import time

from src.handleAwardWeiBo.customFind import FindSingle
from src.handleAwardWeiBo.generalFind import FindAwardWeiBo
from src.systemTools import HandleUserInDatabase, HandleWeiBoInDatabase
from src.systemTools import ReadFileToList


class StartAutoFind(object):
    def __init__(self):
        pass

    def start(self):
        """
        开始调用各种转发方法
        :return:
        """
        self.init_user = HandleUserInDatabase.HandleUserInDatabase().get_total()
        self.init_weibo = HandleWeiBoInDatabase.HandleWeiboInDatabase().get_total()
        # 开始通用搜索，启动单独的线程
        print('\033[33m------------------开始执行通用搜索-------------------\033[0m')
        # FindAwardWeiBo.FindAwardWeiBo().award_run()
        # 读取文件中需要定制查找的用户
        user_list = ReadFileToList.ReadFileInList().read_file('./target_user.txt')
        # 遍历这些用户 进行定制化搜索，不启用单独的线程  在主线程下依次完成
        print('\033[33m------------------开始执行特殊搜索-------------------\033[0m')
        for each in user_list:
            FindSingle.FindSingle().award_run(each)
            time.sleep(10)

        now_user = HandleUserInDatabase.HandleUserInDatabase().get_total()
        now_weibo = HandleWeiBoInDatabase.HandleWeiboInDatabase().get_total()
        print('\033[33m------------------总计处理微博：' + str(now_weibo - self.init_weibo) + '个-------------------\033[0m')
        print('\033[33m------------------总计关注用户：' + str(now_user - self.init_user) + '个-------------------\033[0m')
