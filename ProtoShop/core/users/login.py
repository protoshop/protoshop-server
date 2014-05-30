# -*- coding:utf-8 -*-
import ProtoShop.utils.token as Token
import ProtoShop.conf.global_settings as conf
import datetime
from ProtoShop.utils.views import stringToMD5
from ProtoShop.models.ProtoShop.models import User
from ProtoShop.core.Package import Package
def Login(email='',passwd=''):
	'''
	用户登录

	param email 登录用户名
	param passwd   用户密码（MD5加密）
	'''
	resultDic = Package()
	resultDic.clear()
	try:
		newPasswd = stringToMD5(conf.PASSWD_FIXED_CHARACTER+passwd)
		user = User.objects.get(email=email,password=newPasswd)
		resultDic.status = 0
		result = {}
		token = stringToMD5(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
		Token.save_token(token,user.email)
		result['token'] = token;
		result['email'] = user.email;
		result['name'] = user.name;
		result['nickname'] = user.nickname;
		resultDic.setResult(result)
			
	except (Exception) as e:
		resultDic.status = 1
		resultDic.code = 1002
		resultDic.message = '用户名或密码错误'

	return resultDic