# -*- coding:utf-8 -*-
import pymongo
import time

from src import config
import logging

logging.basicConfig(level=config.LOGGING_LEVEL,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class HandleUserInDatabase(object):
    def __init__(self):
        myclient = pymongo.MongoClient(config.DATABASE_ADDRESS)
        mydb = myclient[config.DATABASE_NAME]
        self.mycol = mydb["User"]

    def save_data(self, uid, name):
        """
        保存uid
        :param uid:
        :return:
        """
        # 检查是否有重复,这里调用前应该检查的，但是重复检查以防出错
        try:
            if len(self.mycol.find_one({"uid": uid})) > 0:
                logging.warning('repeat uid')
                return
        except:
            self.mycol.insert(
                {'uid': uid, 'name': name, 'followed_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})

    def find_data(self, uid):
        """
        查询是否有该uid
        :param uid:
        :return:
        """
        if len(self.mycol.find_one({"uid": uid})) > 0:
            return True
        return False

    def get_total(self):
        """
        返回总共个数
        :return:
        """
        return self.mycol.find().count()
