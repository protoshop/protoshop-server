# -*- coding:utf8 -*-
import ProtoShop.utils.token as Token
from ProtoShop.models.ProtoShop.models import ShareProject,User,Projects
from ProtoShop.utils.views import getCurrentTime
import json
from ProtoShop.core.Package import Package

def shareProject(token='',appid='',user=None,option='',pre=1):
	resultDic = Package()
	resultDic.clear()
	if token == '' or appid == '' or user == None or user == '' or option == '':
		resultDic.status = 1
		resultDic.code = 11002
		resultDic.message = '输入信息不完整'
	else :
		pass
		if not Token.check_token_isvalid(token):
			resultDic.status = 1
			resultDic.code = 11003
			resultDic.message = 'token失效 请重新登录'
			return resultDic
		result = Token.get_token(token)
		useremail = result.userName
		try:
			Projects.objects.get(appid=appid,owner=useremail)
		except (Exception) as e:
			resultDic.status = 1
			resultDic.code = 11004
			resultDic.message = '分享的工程不存在'
			return resultDic
		try:
			'''
			多用户
			'''
			users = json.loads(users)
			for x in range(len(users)):
				resultDic = optionDB(useremail,appid,users[x],option,pre)
		except (Exception) as e:

			'''
			多用户
			'''
			if isinstance(user,list):
				for x in range(len(users)):
					resultDic = optionDB(useremail,appid,users[x],option,pre)
			else:
				'''
				单用户
				'''
				resultDic = optionDB(useremail,appid,user,option,pre)

	return resultDic

def optionDB(owner = '',appid='',user='',option='',pre = 1):
	resultDic = Package()
	resultDic.clear()
	if user == owner:
		resultDic.status = 0
		resultDic.code = 11007
		resultDic.message = '不能给自己分享'
		return resultDic

	hasShare = ShareProject.objects.filter(share_ower=owner,share_user=user,appid=appid)
	if len(hasShare)>0 and option != '2':
		resultDic.status = 1
		resultDic.code = 11005
		resultDic.message = '已经分享过啦'
		return resultDic
	try:
		User.objects.get(email=user)
	except (Exception) as e:
		resultDic.status = 1
		resultDic.code = 11004
		resultDic.message = '分享的用户不存在'
		return resultDic
	
	if option == '1':
		sharepro = ShareProject(appid=appid,share_user=user,share_time=getCurrentTime(),share_ower=owner,permission=pre)
		sharepro.save()
	elif option == '2':
		sharepro = ShareProject.objects.filter(appid=appid,share_user=user,share_ower=owner)
		sharepro.delete()
	else:
		resultDic.status = 1
		resultDic.code = 11006
		resultDic.message = '未知操作'
		return resultDic


	shares = ShareProject.objects.filter(share_ower=owner)
	shareList = []
	for x in range(len(shares)):
		share = shares[x]
		users = User.objects.filter(email=share.share_user)
		for x in range(len(users)):
			user = users[x]
			userDic = {}
			userDic['email'] = '%s'%user.email
			userDic['nickname'] = '%s'%user.nickname
			shareList.append(userDic)

	resultDic.setResult(shareList)

	return resultDic


def shareList(token='',appid =''):
	resultDic = Package()
	resultDic.clear()
	if token == '':
		resultDic.status = 1
		resultDic.code = 12002
		resultDic.message = 'token为空'
	else :
		if Token.check_token_isvalid(token):
			result = Token.get_token(token)
			user = result.userName
			shares = []
			if appid =='':
				shares = ShareProject.objects.filter(share_ower=user)
			else :
				shares = ShareProject.objects.filter(share_ower=user,appid=appid)
			shareList = []
			for x in range(len(shares)):
				share = shares[x]
				users = User.objects.filter(email=share.share_user)
				for x in range(len(users)):
					user = users[x]
					userDic = {}
					userDic['email'] = '%s'%user.email
					userDic['nickname'] = '%s'%user.nickname
					shareList.append(userDic)
			resultDic.setResult(shareList)
		else:
			resultDic.status = 1
			resultDic.code = 12003
			resultDic.message = 'toke失效 请重新登录'

	return resultDic
	



