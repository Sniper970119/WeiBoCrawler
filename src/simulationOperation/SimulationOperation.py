# -*- coding:utf-8 -*-
from src.loginWeiBo import GetCookies
from src.systemTools import LoginWithCookies

# from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random
import time

from src import config
import logging

logging.basicConfig(level=config.LOGGING_LEVEL,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

class SimulationOperation(object):
	"""
	模拟用户行为
	1 home_page 逛首页，完成点赞评论转发等操作
		1.1 每条都点赞
		1.2 随机选择微博评论随机评论内容
		1.3 随机选择微博转发
		1.4 回复评论
	2 逛发现，完成关注点赞评论转发等操作
	3 同步小用户微博
		3.1 获取某用户动态
		3.2 逐条搬运
	4 post_microblog 闲的没事自己发带图片的微博

	"""
	def __init__(self):
		GetCookies.GetCookies()
		pass

	def home_page(self):
		try:
			# 初始化已经带cookies的测试驱动
			self.driver = LoginWithCookies.LoginWithCookies().login_with_cookie()
			# 初始化等待时间，10s
			self.wait = WebDriverWait(self.driver, timeout=10)
			# 获取首页按钮并点击
			self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#weibo_top_public > div > div > div.gn_position > div.gn_nav > ul > li:nth-child(1) > a'))).click()
			logging.info('Found and clicked the home page button')
			# 等待微博内容加载完成（不翻页）
			self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#v6_pl_content_homefeed > div > div.WB_feed.WB_feed_v3.WB_feed_v4')))
			# 开始处理微博
			logging.info('Dealing with microblogs')
			self.soup = BeautifulSoup(self.driver.page_source, 'lxml')
			self.blogs = self.soup.find_all('div', attrs={'action-type':'feed_list_item'})
			# for blog in self.blogs:
			# 	print(blog)
			# 	pass
			# 计数器，用来临时记录转发了多少微博
			j = 0
			for i in range(len(self.blogs)):
				i += j
				logging.info('Dealing with microblog '+str(i+1))
				css_0 = '#v6_pl_content_homefeed > div > div.WB_feed.WB_feed_v3.WB_feed_v4 > div:nth-child(' + str(i+1) + ')'
				# 判断是否为自己转发的微博
				if self.driver.find_element_by_css_selector(css_0+' > div.WB_feed_detail.clearfix > div.WB_detail > div.WB_info > a').get_attribute('title') == '水果皮er':  # ???用户名
					logging.info('This microblog is mine')
					continue
				# 是否评论
				# TODO 评论时有自动转发选项，可以优化提高运行效率
				self.comment_flag = 0
				if random.random()<0.33:
					self.comment_flag = 1
					logging.info('Need comment')
				# 是否转发
				# TODO 转发时有自动评论选项，可以优化提高运行效率
				self.forward_flag = 0
				if random.random() < 0.16:
					self.forward_flag = 1
					logging.info('Need forward')
				# 开始点赞、评论、转发
				# 点赞
				css_1 = ' > div.WB_feed_handle > div > ul > li:nth-child(4) > a > span > span'
				self.css = css_0 + css_1
				# 判断微博是否处理过，是则取消
				if self.driver.find_element_by_css_selector(self.css).get_attribute('title') == '取消赞':
					logging.warning('This microblog has been liked')
					exit(0)
				self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.css))).click()
				logging.info('Liked Successfully')
				time.sleep(15)
				# 评论
				if self.comment_flag:
					css_1 = ' > div.WB_feed_handle > div > ul > li:nth-child(3) > a'
					self.css = css_0 + css_1
					self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.css))).click()
					# TODO 生成评论内容
					css_1 = ' > div.WB_feed_repeat.S_bg1 > div > div > div.WB_feed_publish.clearfix > div.WB_publish'
					self.css = css_0 + css_1
					self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.css+' > div > textarea'))).send_keys('哈哈哈')  # TODO hhh
					time.sleep(10)
					self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.css+' > div.p_opt > div > a'))).click()
					logging.info('Commented Successfully')
					time.sleep(15)
				# 转发
				if self.forward_flag:
					css_1 = ' > div.WB_feed_handle > div > ul > li:nth-child(2) > a'
					self.css = css_0 + css_1
					self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.css))).click()
					# TODO 生成转发内容
					self.wait.until(
						EC.element_to_be_clickable((By.CSS_SELECTOR,
													'div.layer_forward > div > div:nth-child(2) > div > div.WB_feed_repeat.forward_rpt1 > div > div.WB_feed_publish.clearfix > div > div.p_input.p_textarea > textarea'))).send_keys(
						'哈哈哈')  # TODO hhh
					time.sleep(10)
					self.wait.until(
						EC.element_to_be_clickable((By.CSS_SELECTOR,
													'div.layer_forward > div > div:nth-child(2) > div > div.WB_feed_repeat.forward_rpt1 > div > div.WB_feed_publish.clearfix > div > div.p_opt.clearfix > div.btn.W_fr > a'))).click()
					logging.info('Forwarded Successfully')
					time.sleep(30)
					# 因为转发后会自动刷新，自己的微博出现在界面上，所以要+1
					j += 1
				pass
			pass
		except:
			self.error_reason()

	def error_reason(self):
		"""
		判断错误类型
		1.操作过快，请稍后重试
			可能暂停10秒还是过快
		:return:
		"""
		try:
			a = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,' div.content > div:nth-child(3) > div > dl > dd > div')))
			logging.warning('操作过快，请稍后重试！')
			logging.warning(a.text)
			time.sleep(60*5)
			self.home_page()
			pass
		except:
			logging.error('Unkown error occurs')
			exit(-1)
			pass

	def post_microblog(self, texts='哈哈哈', fs='cat.jpg'):
		"""
		发带图片的微博
		:param texts: 文字内容
		:param fs: 图片地址
		:return:
		"""
		try:
			self.driver.get('https://s.weibo.com/')
		except:
			# 初始化已经带cookies的测试驱动
			self.driver = LoginWithCookies.LoginWithCookies().login_with_cookie()
			# 初始化等待时间，10s
			self.wait = WebDriverWait(self.driver, timeout=10)
		# 获取首页按钮并点击
		self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
														'#weibo_top_public > div > div > div.gn_position > div.gn_nav > ul > li:nth-child(1) > a'))).click()
		logging.info('Found and clicked the home page button')
		# 上传文字和图片
		self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#v6_pl_content_publishertop > div > div.input > textarea'))).send_keys(texts)
		time.sleep(10)
		self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#pic_upload > input'))).send_keys(fs)
		logging.info('Upload picture successfully')
		time.sleep(10)
		self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#v6_pl_content_publishertop > div > div.func_area.clearfix > div.func > a'))).click()
		logging.info('Post a microblog successfully')
		time.sleep(10)
		pass

	def stop(self):
		self.driver.quit()
		logging.info('Quit selenium')


if __name__ == '__main__':
	so = SimulationOperation()
	so.home_page()
	so.post_microblog()
	so.stop()
