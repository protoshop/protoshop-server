# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import codecs
import json
from ProtoShop.core.projects.fetchList import fetchProjectList
from ProtoShop.core.projects.project import createProject,saveProject,deleteProject,fetchProject
from ProtoShop.core.Package import Package

@csrf_exempt
def wsFetchProjectList(request):
	#返回给前端的
	resultDic = Package()
	resultDic.clear()
	device = request.GET.get('device','')
	token = request.GET.get('token','')
	if token == '':
		resultDic.status = 1
		resultDic.code = 10001
		resultDic.message = 'token为空'
	else:
		deviceflag = 0
		if device == 'ios':
			deviceflag = 1
		elif device == 'android':
			deviceflag = 2
		resultDic =  fetchProjectList(device = deviceflag, token = token)

	return resultDic.archiveJson()



@csrf_exempt
def wsCreateProject(request):
	#返回给前端的
	resultDic = Package() 
	resultDic.clear()
	#获取JSON
	jsonStr = ''
	if request.POST:
		jsonStr = request.raw_post_data.decode('utf8')
		resultDic = createProject(jsonStr)
	else:
		resultDic.status = 1
		resultDic.code = 6001
		resultDic.message = '请求方式错误'
	return resultDic.archiveJson()


@csrf_exempt
def wsSaveProject(request):
	resultDic = Package()
	resultDic.clear()
	appJson = ''
	if request.POST:
		jsonStr = request.raw_post_data.decode('utf8')
		jsonDic = {}
		try:
			jsonDic = json.loads(jsonStr)
			resultDic = saveProject(jsonDic)
		except (Exception) as e:
			resultDic.status = 1
			resultDic.code = 8002
			resultDic.message = '工程json有格式错误'
	else:
		resultDic.status = 1
		resultDic.code = 8001
		resultDic.message = '请求方式错误'

	return resultDic.archiveJson()


@csrf_exempt
def wsDeleteProject(request):
	resultDic = Package()
	appID = ''
	token = ''
	if request.GET:
		appID = request.GET.get('appid')
		token = request.GET.get('token')
	else:
		resultDic.status = 1
		resultDic.code = 7001
		resultDic.message = '请求方式错误'
	if token == '' or token == None:
		resultDic.status = 1
		resultDic.code = 7002
		resultDic.message = 'token为空'
	if appID == '' or appID == None:
		resultDic.status = 1
		resultDic.code = 7003
		resultDic.message = 'appid为空'
	resultDic = deleteProject(token,appID)

	return resultDic.archiveJson()


@csrf_exempt
def wsFetchProject(request):
	resultDic = Package()
	appid = ''
	token = ''
	if request.GET:
		appid = request.GET.get('appid')
		token = request.GET.get('token')
		resultDic = fetchProject(appid,token)
	else:
		resultDic.status = 1
		resultDic.code = 9001
		resultDic.message = '请求方式错误'

	return resultDic.archiveJson()




