# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ProtoShop.core.projects.share import shareProject,shareList
from ProtoShop.core.Package import Package

@csrf_exempt
def wsShareProject(request):
	resultDic = Package()
	resultDic.clear()
	token = ''
	appid = ''
	user  = ''
	option = ''
	jsonStr = request.raw_post_data.decode('utf8')
	try:
		shareItem = json.loads(jsonStr)
		token  = shareItem['token']
		appid  = shareItem['appid']
		user   = shareItem['user']
		option = shareItem['option']
		pre = shareItem['permission']
	except (Exception) as e:
		if request.POST:
			token  = request.POST.get('token','')
			appid  = request.POST.get('appid','')
			user   = request.POST.get('user','')
			option = request.POST.get('option','')
			pre = request.POST.get('permission')
		else:
			token  = request.GET.get('token','')
			appid  = request.GET.get('appid','')
			user   = request.GET.get('user','')
			option = request.GET.get('option','')
			pre = request.GET.get('permission')
	intPre = 1
	if pre == '2':
		intPre = 2
	resultDic = shareProject(token=token,appid=appid,user=user,option=option,pre = intPre)

	return resultDic.archiveJson()


@csrf_exempt
def wsShareList(request):
	resultDic = Package()
	resultDic.clear()
	token = ''
	appid = ''
	jsonStr = request.raw_post_data.decode('utf8')
	try:
		obj = json.loads(jsonStr)
		token  = obj['token']
		appid  = obj['appid']
	except (Exception) as e:
		if request.POST:
			token  = request.POST.get('token','')
			appid  = request.POST.get('appid','')
		else:
			token  = request.GET.get('token','')
			appid  = request.GET.get('appid','')

	resultDic = shareList(token=token,appid=appid)

	return resultDic.archiveJson()
