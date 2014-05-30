# -*- coding:utf-8 -*-
import ProtoShop.conf.global_settings as conf
import time
import datetime
import ProtoShop.utils.cache as cache

def check_token_isvalid(token):
	'''
	检查token是否有效

	param create_time token创建时间

	return
	'''
	if not check_token_isexist(token):
		return False
	else:
		return True


def check_token_isexist(token):
	'''
	验证token是否存在

	param token 需要验证的token

	return True False
	'''
	return cache.check_key_exists(token)


def save_token(token,userName):
	current = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	values = []
	values.append(userName)
	values.append(current)
	return cache.set_value(token,values)

def get_token(token):
	return cache.get_value(token)

def delete_token(token):
	if cache.delete_value(token):
		return True
	else:
		return False
