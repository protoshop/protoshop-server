# -*- coding:utf8 -*-
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ProtoShop.core.Package import Package
from ProtoShop.core.users.register import Register
from ProtoShop.core.users.login import Login
from ProtoShop.utils.views import validate_email
from ProtoShop.core.users.update import Updatepassword
from ProtoShop.core.users.userinfo import UserInfo,UpdeteInfo

def getIP(request):
	ip = ''
	if 'HTTP_X_FORWARDED_FOR' in request.META.keys():  
		ip =  request.META['HTTP_X_FORWARDED_FOR']  
	else:  
		ip = request.META['REMOTE_ADDR']  
	return ip


@csrf_exempt
def login(request):
	'''
	用户登录接口
	'''
	resultDic = Package()
	resultDic.clear()
	user_email = ''
	user_pwd = ''
	jsonStr = ''
	
	if request.POST:
		jsonStr = request.raw_post_data.decode('utf8')
	else :
		resultDic.status = 1
		resultDic.code = 1001
		resultDic.message = '请求方式不正确'
		return resultDic.archiveJson()

	try:
		loginObj = json.loads(jsonStr)
		user_email = loginObj['email']
		user_pwd = loginObj['passwd']
	except (Exception) as e:
		user_email = request.POST.get('email')
		user_pwd = request.POST.get('passwd')

	if user_email == '' or user_email == None:
		resultDic.status = 1
		resultDic.code = 1003
		resultDic.message = '登录邮箱为空'
	elif user_pwd == '' or user_pwd == None:
		resultDic.status = 1
		resultDic.code = 1004
	else:
		resultDic = Login(email=user_email,passwd=user_pwd)

	return resultDic.archiveJson()

@csrf_exempt
def register(request):
	'''
	用户注册
	'''
	resultDic =  Package()
	resultDic.clear()
	user_name = ''
	user_nick = ''
	user_pwd = ''
	user_email = ''
	jsonStr = ''
		
	if request.POST:
		jsonStr = request.raw_post_data.decode('utf8')
	else :
		resultDic.status = 1
		resultDic.code = 2001
		resultDic.message = '请求方式错误'
		return resultDic.archiveJson()

	try:
		loginObj = json.loads(jsonStr)
		user_pwd = loginObj['passwd']
		user_email = loginObj['email']
		user_nick = loginObj['nickname']
	except (Exception) as e:
		if request.POST:
			user_pwd = request.POST.get('passwd')
			user_email = request.POST.get('email')
			user_nick = request.POST.get('nickname')
		# else:
		# 	user_pwd = request.GET.get('passwd')
		# 	user_email = request.GET.get('email')
		# 	user_nick = request.GET.get('nickname')

	if user_email == '' or user_email == None:
		resultDic.status = 1
		resultDic.code = 2004
		resultDic.message = '邮箱为空'
		return resultDic.archiveJson()
	if not validate_email(user_email):
		resultDic.status = 1
		resultDic.code = 2006
		resultDic.message = '邮箱格式不合法'
		return resultDic.archiveJson()
	if user_pwd == '' or user_pwd == None:
		resultDic.status = 1
		resultDic.code = 2005
		resultDic.message = '用户密码不能为空'
		return resultDic.archiveJson()
	info = {}
	info['user_name'] = user_name
	info['user_nick'] = user_nick
	info['user_pwd'] = user_pwd
	info['user_email'] = user_email
	info['ip'] = getIP(request)
	resultDic = Register(info)

	return resultDic.archiveJson()



@csrf_exempt
def updatepwd(request):
	'''
	修改密码
	'''
	resultDic = Package()
	resultDic.clear()
	token = ''
	newpwd = ''
	if request.POST:
		token = request.POST.get('token','')
		newpwd = request.POST.get('passwd','')
		oldpasswd = request.POST.get('oldpwd','')
	else:
		token = request.GET.get('token','')
		newpwd = request.GET.get('passwd','')
		oldpasswd = request.GET.get('oldpasswd','')
	if token == '' or token == None:
		resultDic.status = 1
		resultDic.code = 3006
		resultDic.message = 'token为空'
	elif newpwd == '' or newpwd == None:
		resultDic.status = 1
		resultDic.code = 3003
		resultDic.message = '新密码为空'
	else:
		resultDic = Updatepassword(token=token,newpwd=newpwd,oldpwd=oldpasswd)
	return resultDic.archiveJson()


@csrf_exempt
def register(request):
	'''
	用户注册
	'''
	resultDic = Package()
	resultDic.clear() 
	user_name = ''
	user_nick = ''
	user_pwd = ''
	user_email = ''

	jsonStr = ''
		
	if request.POST:
		jsonStr = request.raw_post_data.decode('utf8')
	else :
		resultDic.status = 1
		resultDic.code = 2001
		return resultDic.archiveJson()

	try:
		loginObj = json.loads(jsonStr)
		user_pwd = loginObj['passwd']
		user_email = loginObj['email']
		user_nick = loginObj['nickname']
	except (Exception) as e:
		if request.POST:
			user_pwd = request.POST.get('passwd')
			user_email = request.POST.get('email')
			user_nick = request.POST.get('nickname','')
		else:
			user_pwd = request.GET.get('passwd')
			user_email = request.GET.get('email')
			user_nick = request.GET.get('nickname','')

	if user_email == '' or user_email == None:
		resultDic.status = 1
		resultDic.code = 2004
		return resultDic.archiveJson()
	if user_pwd == '' or user_pwd == None:
		resultDic.status = 1
		resultDic.code = 2005
		return resultDic.archiveJson()
	info = {}
	info['user_name'] = user_name
	info['user_nick'] = user_nick
	info['user_pwd'] = user_pwd
	info['user_email'] = user_email
	info['ip'] = getIP(request)
	resultDic = Register(info)
	return resultDic.archiveJson()


@csrf_exempt
def userInfo(request):
	'''
	获取用户信息
	'''
	resultDic = Package() 
	resultDic.clear()
	token = ''
	if request.GET:
		token = request.GET.get('token','')
	else :
		token = request.POST.get('token','')

	if token == '':
		resultDic.status = 1
		resultDic.code = 4001
		resultDic.message = 'token为空 请填写token'
	else:
		resultDic = UserInfo(token = token)

	return resultDic.archiveJson()

@csrf_exempt
def updateInfo(request):
	'''
	获取用户信息
	'''
	resultDic = Package()
	resultDic.clear()
	token = ''
	username = ''
	usernick = ''
	if request.GET:
		token = request.GET.get('token','')
		username = request.GET.get('username','')
		usernick = request.GET.get('nickname','')
	else :
		token = request.POST.get('token','')
		username = request.POST.get('username','')
		usernick = request.POST.get('nickname','')

	if token == '':
		resultDic.status = 1
		resultDic.code = 5001
		resultDic.message = 'toke为空 请填写token'

	else:
		resultDic = UpdeteInfo(token=token,username =username,nickname = usernick)

	return resultDic.archiveJson()
	