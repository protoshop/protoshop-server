# -*- coding:utf8 -*-
import json
from django.http import HttpResponse

class Package(object):
	"""docstring for Package"""
	status = 0;
	code = 0
	message = 'OK'
	result = None
	def __init__(self, status = 0,message = 'OK',result = [],code = 0):
		super(Package, self).__init__()
		self.status = status
		self.message = message
		self.code = 0
		if isinstance(result,list):
			self.result = result
		else:
			self.result = []
			self.result.append(result)

	def setStatus(self,status = 0):
		self.status = status

	def setMessage(self,message = 'OK'):
		self.message = message

	def setResult(self,result = []):
		if isinstance(result,list):
			self.result = result
		else:
			self.result.append(result)

	def archiveJson(self):
		resultDic = {}
		resultDic['status'] = self.status
		resultDic['code'] = self.code
		resultDic['message'] = self.message
		resultDic['result'] = self.result
		resultJson = json.dumps(resultDic)
		return HttpResponse(resultJson,mimetype="text/json")

	def archiveJavaScript(self):
		resultDic = {}
		resultDic['status'] = self.status
		resultDic['code'] = self.code
		resultDic['message'] = self.message
		resultDic['result'] = self.result
		scriptString = ''
		if len(self.result)>0:
			scriptString = '<head><script>var loggedInUser = { \n\
							email: "%(email)s", \
	 				 		name: "%(name)s",\
	  						nickname: "%(nickname)s",\
	  						token: "%(token)s"\
							};	\
							localStorage.setItem(\'loggedInUser\', JSON.stringify(loggedInUser));\n\
							window.location.href="http://protoshop.ctripqa.com/#/list/";</script></head>'%{
							'email':str(resultDic['result'][0]['email']),
							'isSSO':True,
							'name':str(resultDic['result'][0]['name']),
							'nickname':str(resultDic['result'][0]['nickname']),
							'token':str(resultDic['result'][0]['token'])
							}
		else:
			scriptString = '<head><script>\n\
							window.location.href="http://protoshop.ctripqa.com/";</script></head>\n'

		return HttpResponse(scriptString)

	def archiveObj(self):
		resultDic = {}
		resultDic['status'] = self.status
		resultDic['code'] = self.code
		resultDic['message'] = self.message
		resultDic['result'] = self.result
		return resultDic

	def clear(self):
		self.result = None
		self.result = []




		