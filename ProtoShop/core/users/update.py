# -*- coding:utf-8 -*-
import ProtoShop.utils.token as Token
from ProtoShop.models.ProtoShop.models import User
from ProtoShop.utils.views import stringToMD5
import ProtoShop.conf.global_settings as conf
from ProtoShop.core.Package import Package
def Updatepassword(token='',newpwd='',oldpwd=''):
	resultDic = Package()
	resultDic.clear()
	newPasswd = stringToMD5(conf.PASSWD_FIXED_CHARACTER+newpwd)
	oldPasswd = stringToMD5(conf.PASSWD_FIXED_CHARACTER+oldpwd)
	if Token.check_token_isvalid(token):
		try:
			userName = ''
			result = Token.get_token(token)
			userName = result.userName
			user = User.objects.get(email=userName)
			if not user.password == oldPasswd:
				resultDic.status = 1
				resultDic.code = 3004
				resultDic.message = '旧密码不匹配'
				return resultDic
			user.password = newPasswd
			resultDic.status = 0
			resultArray ={}
			resultArray['email'] = user.email
			resultArray['token'] = token
			resultDic.setResult(resultArray)
			user.save()
		except (Exception) as e:
			resultDic.status = 1
			resultDic.code = 3005
			resultDic.message = '服务器内部异常 请稍后再试'
		
	else:
		resultDic.status = 1
		resultDic.code = 3002
		resultDic.message = 'Token无效 请重新登录'

	return resultDic