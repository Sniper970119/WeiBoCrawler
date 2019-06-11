# -*- coding:utf-8 -*-
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["WeiboAward"]
mycol = mydb["Weibo"]