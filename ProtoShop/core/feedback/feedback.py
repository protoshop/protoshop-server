# -*- coding:utf-8 -*-
import ProtoShop.utils.token as Token
from ProtoShop.models.ProtoShop.models import Feedback
from ProtoShop.utils.views import getCurrentTime
from ProtoShop.core.Package import Package

def FeedBack(token = '',email = '',content = '',source = ''):
	resultDic = Package()
	resultDic.clear()
	if content == '' or content == None:
		resultDic.status = 1
		resultDic.code = 13003
		resultDic.message = '内容为空'
		return resultDic
	if source == '' or source == None:
		resultDic.status = 1
		resultDic.code = 13004
		resultDic.message = '来源为空'
		return resultDic

	user = ''
	if token == '' or token == None:
		if email == '' or email == None:
			resultDic.status = 1
			resultDic.code = 13006
			resultDic.message = '邮箱为空'
			return resultDic
		user = email
	else :
		if not Token.check_token_isvalid(token):
			resultDic.status = 1
			resultDic.code = 13002
			resultDic.message = 'toke无效 请重新登录'
			return resultDic
		else :
			result = Token.get_token(token)
			user = result.userName
        	
	try:
		feedback = Feedback(user_name=user,
							   content = content,
							   create_time = getCurrentTime() ,
							   source = source,
		)
		feedback.save()
	except (Exception) as e:
		resultDic.status = 1
		resultDic.code = 13005
		resultDic.message = '服务器内部异常'
	return resultDic