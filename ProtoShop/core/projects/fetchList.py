# -*- coding: utf-8 -*-
from ProtoShop.models.ProtoShop.models import Projects,ShareProject,User
import ProtoShop.utils.token as Token
from django.db.models import Q
from ProtoShop.core.Package import Package

def createProjectDic(project):
	resultProject = {}
	resultProject['appID'] = project.appid
	resultProject['appDesc'] = project.description
	resultProject['appName'] = project.name
	resultProject['appIcon'] = project.icon
	if project.platform == 1:
		resultProject['appPlatform'] = 'ios'
	if project.platform == 2:
		resultProject['appPlatform'] = 'android'
	resultProject['createTime'] = project.create_time
	resultProject['editTime'] = project.edit_time
	if project.public == 1:
		resultProject['isPublic'] = '0'
	if project.public == 2:
		resultProject['isPublic'] = '1'
	resultProject['appOwner'] = project.owner
	user = User.objects.get(email = project.owner) 
	resultProject['appOwnerNickname'] = user.nickname
	return resultProject

def fetchProjectList(device = '',token = ''):
	resultDic = Package()
	resultDic.clear()
	if not Token.check_token_isvalid(token):
		resultDic.status = 1
		resultDic.code = 10002
		resultDic.message = 'token失效 请重新登录'
	else:
		ower = ''
		result = Token.get_token(token)
		ower = result.userName
		projects = []
		resultList = []
		
		try:
			if device == 0:
				projects = Projects.objects.filter(Q(owner=ower)|Q(public=2))
			else :
				projects = Projects.objects.filter(Q(owner=ower,platform=device)|Q(public=2,platform=device))
			for x in range(len(projects)):
				project = projects[x]
				resultList.append(createProjectDic(project))
			shareprojects = ShareProject.objects.filter(share_user=ower)
			for y in range(len(shareprojects)):
				share = shareprojects[y]
				project =  Projects.objects.get(appid=share.appid)
				resultList.append(createProjectDic(project))

			resultDic.setResult(resultList)
		except (Exception) as e:
			resultDic.status = 1
			resultDic.code = 10007
			resultDic.message = '服务器内部错误'
	
	return resultDic
