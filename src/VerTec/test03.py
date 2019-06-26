import configparser
import re

# cf = configparser.ConfigParser()
# cf.read('../../friends.ini', encoding='utf-8')
# friend_1 = cf.get('FRIENDS', 'friend_1')
# friend_2 = cf.get('FRIENDS', 'friend_2')
# print(friend_1, friend_2)

text = "车$专CONFIG['oid']='119504454'"
text1 = """
[
<div action-data="uid=1746575865&amp;fnick=互联网俊明说&amp;f=1&amp;refer_flag=1005050001_&amp;refer_lflag=1001030103_&amp;refer_from=profile_headerv6&amp;template=7&amp;nogroup=1&amp;special_focus=1&amp;isrecommend=1&amp;is_special=0&amp;redirect_url=%2Fp%2F1005055123485468%2Fmyfollow%3Fgid%3D3739420521408994%23place"
     class="btn_bed W_fl" node-type="focusLink">

    <a action-type="unFollow" class="W_btn_d btn_34px" href="javascript:void(0);"
       suda-data="key=tblog_attention_click&amp;value=1746575865"><em class="W_ficon ficon_right S_ficon">Y</em>已关注</a>
    <a action-data="uid=1746575865&amp;refer_from=profile_headerv6" action-type="follow_recommend_arr"
       class="W_btn_d btn_34px btn_opt" href="javascript:void(0);"><em class="W_ficon ficon_arrow_down_lite"
                                                                       suda-uatrack="key=wb_pc_profile&amp;value=atten_down">g</em></a>
</div>]"""
# print(re.findall("CONFIG['oid']='(.*?)'", text))
# print(re.findall("uid=(.*?)&", text1))
print(re.findall("车.{0,3}专", text))
