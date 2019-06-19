import random

import pymongo
import time

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["WeiboAward"]
# mycol = mydb["User"]
# # mycol.insert({'uid': '123456', 'forward_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
# print(mycol.find_one({"uid": "123456"}))
# print(type(mycol.find_one({"uid": "123456"})))

print(''.join(random.sample('0123456789', 5)))
