# -*- coding: utf-8 -*-
import time
import hashlib
import re

#获取时间MD5接口
def getTimeMD5():
	createTime = time.time()
	createTimeStr = '%f'%createTime
	hashObj = hashlib.md5(createTimeStr.encode("utf8"))
	md5Str = hashObj.hexdigest()
	return md5Str


#获取当前时间格式为 xxxx-xx-xx xx:xx:xx
def getCurrentTime():
	timeStr = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())) 
	return timeStr


#检测邮箱是否合法
def validate_email(inputMail):
	isMatch = bool(re.match(r"^[a-zA-Z](([a-zA-Z0-9]*\.[a-zA-Z0-9]*)|[a-zA-Z0-9]*)[a-zA-Z]@([a-z0-9A-Z]+\.)+[a-zA-Z]{2,}$", inputMail,re.VERBOSE))
	return isMatch

#MD5加密
def stringToMD5(inputStr):
	hashObj = hashlib.md5(inputStr.encode("utf-8"))
	md5Str = hashObj.hexdigest()
	return md5Str

def getIP(request):
	ip = ''
	if 'HTTP_X_FORWARDED_FOR' in request.META.keys():  
		ip =  request.META['HTTP_X_FORWARDED_FOR']  
	else:  
		ip = request.META['REMOTE_ADDR']  
	return ip
	

