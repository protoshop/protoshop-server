# -*- coding: utf-8 -*-
import json
import os
import time
import hashlib
from io import BytesIO
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt
from .forms.UploadFileForm import UploadFileForm
import ProtoShop.conf.global_settings as CONFIG
from ProtoShop.core.Package import Package

def handle_uploaded_file(f,projectName):
	createTime = time.time()
	createTimeStr = '%f'%createTime
	hashObj = hashlib.md5(createTimeStr.encode("gb2312"))
	md5Str = hashObj.hexdigest()

	with open(CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH+projectName+'/'+md5Str+'.png', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	return md5Str

def parserHTTPRequest(request):
	flag = 0;
	try:
		result = ''
		total = len(request.raw_post_data)
		stream = BytesIO(request.raw_post_data)

		result = stream.readline()
		length = len(result)
		#分割符号长度
		separatedLen = length
		total = total - length
		result = stream.readline()
		length = len(result)
		total = total - length
		result = stream.readline()
		length = len(result)
		total = total - length

		#Appid 数据行
		result = stream.readline()
		appid = u'%s'%result
		appid = appid.replace("b'",'')
		length = len(result)
		total = total - length
		appid = appid.strip()
		
		result = stream.readline()
		length = len(result)
		total = total - length
		result = stream.readline()
		length = len(result)
		total = total - length
		result = stream.readline()
		length = len(result)
		total = total - length

		#imageName 数据行
		result = stream.readline()
		imageName = u'%s'%result
		imageName = imageName.replace("b'",'')
		imageName = imageName.strip()
		# return imageName
		length = len(result)
		total = total - length

		#如果图片名称不为空 删除文件
		if len(imageName) > 0:
			#删除以前的图片文件
			fileName = CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH + appid +'/' + imageName
			if os.path.exists(fileName):
				os.remove(fileName)
				
		result = stream.readline()
		length = len(result)
		total = total - length
		result = stream.readline()
		length = len(result)
		total = total - length
		#图片标示的数据行
		result = stream.readline()
		length = len(result)
		total = total - length
		result = stream.readline()

		length = len(result)
		total = total - length

		#图片所在的数据行
		result = stream.read(total-separatedLen)
		createTime = time.time()
		createTimeStr = '%f'%createTime
		hashObj = hashlib.md5(createTimeStr.encode("gb2312"))
		md5Str = hashObj.hexdigest()
		filename = CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH+appid+'/'+md5Str+'.png'
		f=open(filename,'wb')
		f.write(result)
		f.close();

		flag = appid+'+'+md5Str+'.png'
	except (Exception) as e:
		flag = str(e)
	return flag


@csrf_exempt
def wsUploadImage(request):
	#返回给前端的
	resultDic = Package()
	resultDic.clear()
	# resultDic.message = parserHTTPRequest(request)
	# return resultDic.archiveJson()
	appid = ''
	if request.method == 'POST':
		try:
			appid = request.POST.get('appid')
			form = UploadFileForm(request.POST,request.FILES)
			if form.is_valid():
				fileName = ''
				fileName = handle_uploaded_file(request.FILES['file'],appid)
				return HttpResponseRedirect('http://wxddb1.qa.nt.ctripcorp.com/api/uploader/success.html#'+fileName)
			else:
				resultDic['status'] = '0'
				
		except (Exception) as e:
			flag = parserHTTPRequest(request)
			if flag == '0':
				resultDic.status = 1
				resultDic.message = flag#'上传图片出错'
			else:
				resultList = flag.split('+')
				resultDic.status = 0
				fileName = ''
				if len(resultList) >= 2:
					appid    = resultList[0]
					fileName = resultList[1]

				resultDictory = {}
				resultDictory['fileName'] = fileName
				resultDictory['appid'] = appid
				resultDic.setResult(resultDictory)

	else:
		resultDic.status = 1
		resultDic.message = '请求方式不对'

	return resultDic.archiveJson()

	