# -*- coding:utf-8 -*-

import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
    'Cookie': 'blog.csdn.net,widget.weibo.com,login.sina.com.cn; SINAGLOBAL=3755037512343.2812.1519369021129; ULV=1560085514189:20:2:2:4195897423244.42.1560085514172:1560048043125; SCF=AqsaV9LwZxR9PQcOz2arJcpSAiVoqhY6xsWh5IRYKMIGNWUIbRp1SXwJMO0mvbb5WxX_2xXf0i9P8w_fbPTjuuU.; SUHB=0oUp-mdsgaSqNx; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ELXNzeq6ma_-JYkQSczuJ5JpX5KMhUgL.FozcSKqESo5fS022dJLoIN-LxK.L1KeL1h2LxKqL1-qLBo2LxKqL1-eLB-2LxKqL1-BLBK-LxKMLBKML1K2LxKqL122L1h5LxKqL1-eL1h.LxK.L1K.L1K5LxK-L1h-LB-eLxK-L12qLBonLxKnL1K2LBKeLxKBLB.2L12zLxK.L1K-LB.qt; ALF=1591621512; UM_distinctid=16ae8938e7b26f-01febfbd58d2d08-4c312c7c-1fa400-16ae8938e7c31b; wb_view_log_2656260571=1920*10801; webim_unReadCount=%7B%22time%22%3A1560085679808%2C%22dm_pub_total%22%3A0%2C%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D; SUB=_2A25x-XRYDeRhGeRI7lQT9i7JzD2IHXVSj-KQrDV8PUNbmtAKLRTykW9NUrGLcWkxPqlDMJdT2gqv6Yx9nOctvaSR; SSOLoginState=1560085512; _s_tentry=login.sina.com.cn; Apache=4195897423244.42.1560085514172; TC-V5-G0=4e714161a27175839f5a8e7411c8b98c; TC-Page-G0=2f200ef68557e15c78db077758a88e1f|1560085678|1560085517',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://weibo.com/2656260571/profile?topnav=1&wvr=6&is_all=1'

}

data = {
    'pic_src': '',
    'pic_id': '',
    'appkey': '',
    'mid': '4380687744180681',
    'style_type': '1',
    'mark': '',
    'reason': '123',
    'location': 'page_100505_home',
    'pdetail': '1005052656260571',
}

import json
r = requests.post('https://weibo.com/aj/v6/mblog/forward?ajwvr=6', data=json.dumps(data), headers=header)
