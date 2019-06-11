import configparser

cf = configparser.ConfigParser()
cf.read('../../friends.ini', encoding='utf-8')
friend_1 = cf.get('FRIENDS', 'friend_1')
friend_2 = cf.get('FRIENDS', 'friend_2')
print(friend_1, friend_2)
