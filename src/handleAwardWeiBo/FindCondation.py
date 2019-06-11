# -*-coding:utf-8 -*-
import re


class FindCondation(object):
    """
    判断抽奖条件
    """

    def __init__(self):
        pass

    def find_condation(self, weibo_list, weibo_main_body):
        # 转发条件
        condation = []
        # 遍历微博列表
        for i in range(0, len(weibo_list)):
            temp_dir = {}
            # 判断正文中是否出现这种字眼
            have_zan = len(re.findall('赞', weibo_main_body[i]))
            have_guan = len(re.findall('关', weibo_main_body[i]))
            have_zhu = len(re.findall('注', weibo_main_body[i]))
            have_zhuan = len(re.findall('转', weibo_main_body[i]))
            have_you = len(re.findall('友', weibo_main_body[i]))
            need_attention = re.findall('@(.{1,20})</a>', weibo_main_body[i], re.S)
            # 判断是否需要点赞操作
            if have_zan > 0:
                temp_dir['need_zan'] = '1'
            else:
                temp_dir['need_zan'] = '0'
            # 判断是否需要关注
            if have_guan > 0 or have_zhu > 0:
                temp_dir['need_attention'] = '1'
            else:
                temp_dir['need_attention'] = '0'
            # 判断是否需要转发
            if have_zhuan > 0:
                # 需要转发默认需要关注
                temp_dir['need_forward'] = '1'
                temp_dir['need_attention'] = '1'
            else:
                temp_dir['need_forward'] = '0'
            # 判断是否需要at好友
            if have_you > 0:
                temp_dir['need_at_friend'] = '1'
            else:
                temp_dir['need_at_friend'] = '0'
            # 增加关注列表
            temp_dir['attention_list'] = need_attention
            condation.append(temp_dir)
        return condation
        pass
