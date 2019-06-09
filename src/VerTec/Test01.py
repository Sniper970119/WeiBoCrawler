# -*- coding:utf-8 -*-
import urllib.parse

# # 关键字编码
# keyword_change = urllib.parse.quote_plus('抽奖')
# keyword_change = urllib.parse.quote_plus(keyword_change)
# # 构建URL
# url = 'https://s.weibo.com/weibo/' + keyword_change + '&xsort=hot&page=%s' % (str(1))
#
# print(url)

text = """
</div>
</div>
<p class="txt" node-type="feed_list_content" nick-name="浙江大学">
数学考完啦，你一定有超常发挥对不对！
来，让小浙和头条君为你送上数学学科“满分祝福”！高考数学150分，我们【抽20位粉丝获得150元“满分祝福红包”】
关注@浙江大学@头条新闻，并@ 你想传递高考祝福的两个好友，就可以参与抽奖啦！#高校官微发满分祝福红包# 
6月15日中午12:00@微博抽奖平 展开全文
</p>
<p class="txt" node-type="feed_list_content_full" nick-name="浙江大学"style="display: none">
数学考完啦，你一定有超常发挥对不对！
来，让小浙和头条君为你送上数学学科“满分祝福”！高考数学150分，我们【抽20位粉丝获得150元“满分祝福红包”】
关注@浙江大学@头条新闻，并@ 你想传递高考祝福的两个好友，就可以参与抽奖啦！#高校官微发满分祝福红包#
6月15日中午12:00@微博抽奖平台开！
既然说到数学，那小浙可要好好夸夸自己。
著名数学家陈建功和苏步青创立的“陈苏学派”享誉世界，浙里有程民德、谷超豪、夏道行、王元等院士，
林芳华、励建书、汪徐家等国际杰出青年数学家，更有网红数学教授
@浙江大学苏德矿人气助力！快来转发，接受来自数学学科大神@浙江大学的高考数学满分祝福吧！#高考加油#@微博校园
</p>
<!--card解析-->
"""
import re
weibo_main_body = re.findall('<p class="txt".*>(.*)</p>\s<!--card解析-->', text)
print(len(weibo_main_body))
print(weibo_main_body)