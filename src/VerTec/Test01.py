# -*- coding:utf-8 -*-
import urllib.parse

# 关键字编码
keyword_change = urllib.parse.quote_plus('抽奖')
keyword_change = urllib.parse.quote_plus(keyword_change)
# 构建URL
url = 'https://s.weibo.com/weibo/' + keyword_change + '&xsort=hot&page=%s' % (str(1))

print(url)