# -*- coding: utf-8 -*-
import os
import sys
from django.http import HttpResponse
import json
import ProtoShop.middleware.parser.iOSParser as iOS
import ProtoShop.middleware.parser.AndroidParser as Android
import ProtoShop.middleware.parser.wsFileUtil as fileUtil
from django.views.decorators.csrf import csrf_exempt
import ProtoShop.conf.global_settings as CONFIG
import codecs 
default_encoding = 'utf8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
#Python入口函数
def readFile(fileName):
	result = ''
	file_handler = codecs.open(fileName,'r',"utf-8")
	try:
		result = file_handler.read()
	finally:
		file_handler.close()
	return result

def wsParser(appID,userName):
	resultFlag = 0
	jsonStr = ''
	
	fileName = CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH+appID+'/projectJson.json'
	# fileName = '/var/www/ProtoShop/packages/ProjectDemo.json'
	jsonStr = readFile(fileName)

	try:
		projectObj = json.loads(jsonStr)
		platform = projectObj['appPlatform']
		projectObj['appID'] = appID
		if platform == 'ios':
			flag = iOS.feed(userName,projectObj)
			resultFlag = flag
		elif platform == 'android':
			flag = Android.feed(userName,projectObj)
			resultFlag = flag
		else:
			resultFlag = 0
			
	except (Exception) as e: 
		 resultFlag = str(e)
	return resultFlag

