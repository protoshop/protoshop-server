# -*- coding:utf8 -*-
from django.http import HttpResponse
from django.db import connection
import json
import MySQLdb
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def Hello(request):
	resultStr = '<br><br><br><center><h1>Hi,Welcome ProtoShop API.</h1></center><br>'
	
	return HttpResponse(resultStr,mimetype="text/html")

@csrf_exempt
def auth(request):
	pass
	
	resultDic = {}
	username = '%s'%request.user
	if username == 'AnonymousUser':
		return HttpResponse('1002')
	else:
		conn=MySQLdb.connect(host='localhost',user='root',passwd='wxd!333333',db='ProtoShop_test',port=3306,charset='utf8')
		cur=conn.cursor()
		cur.execute("select * from auth_user where username = '%s'"%username)
		result =  cur.fetchone(); 
		cur.close()
		conn.close()
		resultDic['status'] = '1001'
		resultDic['result'] = {}
		resultDic['result']['username'] = result[4]
		resultDic['result']['compayID'] = result[5]
		resultDic['result']['nickName'] = result[6].encode('utf8')
		resultDic['result']['email'] = result[7]
	return HttpResponse(json.dumps(resultDic))
	
