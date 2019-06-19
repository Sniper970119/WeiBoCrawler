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
        self.mycol = mydb["User"]

    def save_data(self, uid):
        """
        保存uid
        :param uid:
        :return:
        """
        # 检查是否有重复,这里调用前应该检查的，但是重复检查以防出错
        try:
            if len(self.mycol.find_one({"uid": uid})) > 0:
                logging.error('repeat uid')
                return
        except:
            self.mycol.insert({'uid': uid, 'forward_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})

    def find_data(self, uid):
        """
        查询是否有该uid
        :param uid:
        :return:
        """
        if len(self.mycol.find_one({"uid": uid})) > 0:
            return True
        return False

