# -*- coding:utf-8 -*-
import ProtoShop.utils.token as Token
from ProtoShop.models.ProtoShop.models import User
import ProtoShop.conf.global_settings as conf
from ProtoShop.utils.views import stringToMD5,getCurrentTime
import datetime
from ProtoShop.core.Package import Package

def Register(userInfo):
	resultDic = Package()
	resultDic.clear()
	try:
		user = User.objects.get(email=userInfo['user_email'])
		resultDic.status = 1
		resultDic.code = 2002
		resultDic.message = '您注册的用户已存在'
	except (Exception) as e:
		try:
			user_pwd = stringToMD5(conf.PASSWD_FIXED_CHARACTER+userInfo['user_pwd'])
			user = User(name=userInfo['user_name'],
				         email= userInfo['user_email'],
				         nickname=userInfo['user_nick'],
				         password=user_pwd,
				         create_time=getCurrentTime(),
				         edit_time=getCurrentTime(),
				         last_login_time = getCurrentTime(),
				         login_source = 1,
				         signin_source = 2,
				         signin_ip = userInfo['ip'],
				         userid='000000',
				         is_ctrip = 1,
				         )
			user.save()
			token = stringToMD5(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
			Token.save_token(token,userInfo['user_email'])
			resultInfo = {}
			resultInfo['token'] = token
			resultInfo['name'] = userInfo['user_name']
			resultInfo['nickname'] = userInfo['user_nick']
			resultInfo['email'] = userInfo['user_email']
			resultDic.setResult(resultInfo)

		except (Exception) as e:
			resultDic.status = 1
			resultDic.code = 2003
			resultDic.message = '服务器内部错误'


	return resultDic