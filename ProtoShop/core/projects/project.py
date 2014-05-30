# -*- coding:utf8 -*-
from ProtoShop.models.ProtoShop.models import Projects,ShareProject
import ProtoShop.utils.token as Token
import ProtoShop.conf.global_settings as CONFIG
from ProtoShop.utils.views import getTimeMD5,getCurrentTime
import json
import os
import codecs 
import shutil
import time
from ProtoShop.core.Package import Package
'''
内部使用函数
'''
def saveProjectWith(json_obj,appid,appOwner):
	plantform = 0
	secret = 0
	if json_obj['package']['appPlatform'] == 'ios':
		plantform = 1
	elif json_obj['package']['appPlatform'] == 'android':
		plantform = 2

	if not json_obj['package']['isPublic']:
		secret = 1
	else:
		secret = 2

	project = Projects(appid=appid,
					   description=json_obj['package']['appDesc'],
					   name=json_obj['package']['appName'],
					   icon=CONFIG.PROJECT_ICON_URL,
					   platform=plantform,
					   create_time=getCurrentTime(),
					   edit_time=getCurrentTime(),
					   public=secret,
					   owner=appOwner,
					   path=CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH + appid +'/'
					   )
	project.save()


def writeFile(fileName,jsonStr):
	file_handler =  codecs.open(fileName, 'w',"utf-8")
	file_handler.write(jsonStr)
	file_handler.close()

#获取文件内容
def readFile(fileName):
	result = ''
	file_handler = codecs.open(fileName,'r',"utf-8")
	try:
		result = file_handler.read()
	finally:
		file_handler.close()
	return result

'''
内部使用函数结束
'''
def createProject(info):
	resultDic = Package()
	resultDic.clear()
	json_obj = json.loads(info)
	token = json_obj['context']['token']
	if not Token.check_token_isvalid(token):
		resultDic.status = 1
		resultDic.code = 6002
		resultDic.message = 'token失效 请重新登录'
		return resultDic

	try:
		#获取文件路径
		path = CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH
		folderName =  getTimeMD5()

		new_path = os.path.join(path,folderName)
		if not os.path.isdir(new_path):
			os.makedirs(new_path)

		#将工程配置文件写入
		projectDic = {}
		projectDic['appID'] = folderName
		projectDic['appName'] = json_obj['package']['appName']
		projectDic['appPlatform'] = json_obj['package']['appPlatform']
		projectDic['appIcon'] = CONFIG.PROJECT_ICON_URL
		projectDic['splash'] = {}
		projectDic['splash']['image'] = ''
		projectDic['splash']['delay'] = ''
		projectDic['splash']['duration'] = ''
		projectDic['splash']['transferType'] = ''
		sizeDic = {}
		sizeDic['width'] = json_obj['package']['size']['width']
		sizeDic['height'] = json_obj['package']['size']['height']
		projectDic['size'] = sizeDic
		scenesDic = {}	
		scenesDic['id'] = '%d00'%time.time()
		scenesDic['order'] = 0
		scenesDic['name'] = 'Scene 1'
		scenesDic['background'] = ''
		scenesDic['elements'] = []
		projectDic['scenes'] = [scenesDic]

		projectFileName = CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH + folderName + '/projectJson.json'
		file_handler =  codecs.open(projectFileName, 'w',"utf-8")
		file_handler.write(json.dumps(projectDic))
		file_handler.close()

		resultDictory = {}
		resultDictory['appID'] = folderName;
		resultDictory['appName'] = json_obj['package']['appName']
		resultDictory['appPlatform'] = json_obj['package']['appPlatform']
		resultDic.setResult(resultDictory)

		userName = ''
		result = Token.get_token(token)
		userName = result.userName
		#将此配置列表写入
		saveProjectWith(json_obj,folderName,userName)
	
	except (Exception) as e: 
		resultDic.status = 1
		resultDic.code = 6003
		resultDic.message = '服务器内部异常'
	return resultDic


def saveProject(info):
	token = info['context']['token']
	resultDic = Package()
	resultDic.clear()
	if not Token.check_token_isvalid(token):
		resultDic.status = 1
		resultDic.code = 8003
		resultDic.message = 'token失效 请重新登录'
		return resultDic

	try:
		appID = info['package']['appID']
		userName = ''
		result = Token.get_token(token)
		userName = result.userName

		project = Projects.objects.get(appid=appID,owner=userName)
		fileName = CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH+appID+'/projectJson.json'
		writeFile(fileName,json.dumps(info['package']))
		project.edit_time = getCurrentTime()
		project.save()
	except (Exception) as e:
		resultDic.status = 1
		resultDic.code = 8004
		resultDic.message = '你不是当前工程的拥有者不能修改'

	return resultDic
		
	


def deleteProject(token,appID):
	resultDic = Package()
	resultDic.clear()
	if not Token.check_token_isvalid(token):
		resultDic.status = 1
		resultDic.code = 7004
		resultDic.message = 'token失效 请重新登录'
		return resultDic
	try:
		userName = ''
		result = Token.get_token(token)
		userName = result.userName	
		project = Projects.objects.get(appid=appID,owner=userName)
		project.delete()
		share_project = ShareProject.objects.filter(appid=appID)
		share_project.delete()
		#删除文件夹
		Dir = CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH+appID
		shutil.rmtree(Dir)#删除
		#删除ZIP文件
		zipFileName = CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH + appID + '.zip'
		if os.path.exists(zipFileName):
			os.remove(zipFileName)
		
	except (Exception) as e:
		resultDic.status = 1
		resultDic.code = 7005
		resultDic.message = '您不是此工程的拥有者，不能删除此工程 ^^'

	return resultDic



def fetchProject(appid,token):
	resultDic = Package()
	resultDic.clear()
	if not Token.check_token_isvalid(token):
		resultDic.status = 1
		resultDic.code = 9002
		resultDic.message = 'token失效 请重新登录'
		
	else :
		#返回给前端的
		try:
			fileName = CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH+appid+'/projectJson.json'
			result = readFile(fileName)
			resultObj = json.loads(result)
			resultDic.setResult(resultObj)
		except (Exception) as e:
			resultDic.status = 1
			resultDic.code = 9003
			resultDic.message = '服务器内部异常'
	return resultDic


			