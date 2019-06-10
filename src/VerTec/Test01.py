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

# weibo_main_body = re.findall('<p class="txt".*>(.*)</p>\s<!--card解析-->', text)
# print(len(weibo_main_body))
# print(weibo_main_body)
text1 = 'target="_blank">@叫我马买买</a> <b'
# need_attention = re.findall('@(.*?)</a>', text1)
# print(need_attention)
text2 = """
<p class="txt" nick-name="钱哥" node-type="feed_list_content">
                    暴富机会来了 豪送30000[小仙女]   <br/>   <br/>转这条 同时关注 我和 <a href="//weibo.com/n/%E7%BE%8E%E5%B0%91%E5%A5%B3Lisa%E9%85%B1" target="_blank">@美少女Lisa酱</a>  <br/>6.24至6.29每天抽一人打5000 连续6天~   <br/>   <br/>通过<a href="//weibo.com/n/%E5%BE%AE%E5%8D%9A%E6%8A%BD%E5%A5%96%E5%B9%B3%E5%8F%B0" target="_blank">@微博<em class="s-color-red">抽奖</em>平台</a> 公开 你将会是下一条锦鲤<img alt="[锦鲤]" class="face" src="//img.t.sinajs.cn/t4/appstyle/expression/ext/normal/94/hbf2019_jinli_org.png" title="[锦鲤]"/> ​ ​​​                </p>
"""
user = re.findall('@(.{1,20})</a>', text2, re.S)
print(user)
