# -*- coding:utf8 -*-
import ProtoShop.utils.token as Token
from ProtoShop.models.ProtoShop.models import User
from ProtoShop.utils.views import getCurrentTime
from ProtoShop.core.Package import Package

def UserInfo(token = ''):
	resultDic = Package()
	resultDic.clear()
	if Token.check_token_isvalid(token):
		try:
			userName = ''
			result = Token.get_token(token)
			userName = result.userName
			user = User.objects.get(email=userName)
			resultDic.status = 0
			resultArray = {}
			resultArray['name'] = user.name
			resultArray['nickname'] = user.nickname
			resultArray['email'] = user.email
			resultArray['createtime'] = user.create_time
			resultArray['userid'] = user.userid
			resultDic.setResult(resultArray)
		except (Exception) as e:
			resultDic.status = 1
			resultDic.code = 4003
			resultDic.message = '服务器内部错误'
		
	else:
		resultDic.status = 1
		resultDic.code = 4002
		resultDic.message = 'token无效 请重新登录'
	return resultDic



def UpdeteInfo(token = '' ,username ='',nickname = ''):
	resultDic = Package()
	resultDic.clear()
	if Token.check_token_isvalid(token):
		try:
			userName = ''
			result = Token.get_token(token)
			userName = result.userName
			user = User.objects.get(email=userName)
			user.name = username
			user.nickname = nickname
			user.edit_time = getCurrentTime()
			user.save()
			resultDic.status = 0
		except (Exception) as e:
			resultDic.status = 1
			resultDic.code = 5003
			resultDic.message = '服务器内部错误'

	else:
		resultDic.status = 1
		resultDic.code = 5002
		resultDic.message = 'token无效 请重新登录'

	return resultDic



