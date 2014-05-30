# -*- coding:utf-8 -*-
import redis
import types
import ProtoShop.conf.global_settings as conf

class TokenModel(object):
	"""docstring for TokenModel"""
	def __init__(self):
		super(TokenModel, self).__init__()
		self.token = ''
		self.userName = ''
		self.create_time = ''
	def createDic(self):
		result ={}
		result['userName'] = self.userName
		result['token'] = self.token
		result['create_time'] = self.create_time
		return result

	@staticmethod
	def createTokenModel(info):
		model = TokenModel()
		model.userName = info['userName']
		model.token = info['token']
		model.create_time = info['create_time']
		return model



def connect_redis():
	try:
		pool = redis.ConnectionPool(host = conf.REDIS_HOST, port = conf.REDIS_PORT, db = conf.REDIS_DB)
		conn  = redis.Redis(connection_pool = pool)
		return conn
	except (Exception) as e:
		return None
	

def set_value(key,value):
	'''
	设置token

	param key     关键字
	param value   值

	return True or False
	'''
	r = connect_redis()
	if r.exists(key):
		return False

	if isinstance(value, list):
		valuelen = len(value)
		value.reverse()
		for i in range(valuelen):
			r.lpush(key, value[i])
		r.expire(key,conf.MAX_TOKEN_EFFECTIVE_TIME)
		return True
	else :
		return False

	
def get_value(key):
	'''
	获取token

	param key     关键字
	param token   token

	return 存在toke返回 不存在则返回空
	'''
	r = connect_redis()
	value = []
	valuelen = r.llen(key)
	for i in range(valuelen):
		result = '%s'%r.lindex(key, i).decode('UTF-8')
		value.append(result)
	result = TokenModel()
	result.userName = value[0]
	result.token = key
	result.create_time = value[1]
	return result


def check_key_exists(key):
	r = connect_redis()
	return r.exists(key)

def delete_value(key):
	r = connect_redis()
	if r.delete(key):
		return True
	else:
		return False
