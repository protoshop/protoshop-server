# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ProtoShop.core.feedback.feedback import FeedBack
from ProtoShop.core.Package import Package
import json
@csrf_exempt
def wsFeedBack(request):
	resultDic = Package()
	resultDic.clear()
	if request.POST:
		source = request.POST.get('source')
		content = request.POST.get('content')
		token = request.POST.get('token')
		email = request.POST.get('email')
		resultDic = FeedBack(token = token,email = email,content = content,source = source)
	else:
		resultDic.status = 1
		resultDic.code = 13001
		resultDic.message = '请求方式正确'
	return resultDic.archiveJson()
	