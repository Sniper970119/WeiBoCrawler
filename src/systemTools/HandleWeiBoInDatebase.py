# -*- coding:utf-8 -*-
import pymongo
import time

from src import config
import logging

logging.basicConfig(level=config.LOGGING_LEVEL,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class HandleUserInDatabase(object):
    def __init__(self):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["WeiboAward"]
        self.mycol = mydb["Weibo"]

    def save_data(self, mid):
        """
        保存uid
        :param mid:
        :return:
        """
        # 检查是否有重复,这里调用前应该检查的，但是重复检查以防出错
        try:
            if len(self.mycol.find_one({"mid": mid})) > 0:
                logging.error('repeat mid')
                return
        except:
            self.mycol.insert(
                {'mid': mid, 'forward_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})

    def find_data(self, mid):
        """
        查询是否有该uid
        :param mid:
        :return:
        """
        try:
            if len(self.mycol.find_one({"mid": mid})) > 0:
                return True
        except:
            return False

    def if_have_data_and_save_it(self, mid):
        """
        判断是否存在该条数据，如果存在返回T，不存在保存后返回F
        :return:
        """
        try:
            if len(self.mycol.find_one({"mid": mid})) > 0:
                logging.error('weibo has been handled')
                return True
        except:
            self.mycol.insert(
                {'mid': mid, 'forward_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
            return False
