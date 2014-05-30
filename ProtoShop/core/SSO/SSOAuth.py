# -*- conding:utf8 -*-
from django.http import HttpResponse
import ProtoShop.utils.token as Token
from ProtoShop.models.ProtoShop.models import User
import ProtoShop.conf.global_settings as conf
from ProtoShop.utils.views import stringToMD5,getCurrentTime
import datetime
from ProtoShop.core.Package import Package
import MySQLdb

def AuthTest(request):
	resultStr = ''
	
	username = '%s'%request.user
	if username == 'AnonymousUser':
		resultStr = 'Logout Success.'
	else:
		resultStr = 'Login Success: %s'%username
	
	return HttpResponse(resultStr)


def SSOAuthCallBack(request):	
	fromSource = ''
	if request.GET:
		fromSource = request.GET.get('type','')

	resultDic = Package()
	resultDic.clear()
	username = '%s'%request.user
	if username == 'AnonymousUser':
		resultDic.status = 1
		resultDic.code = 1002
		resultDic.message = ''
	else:
		
		conn=MySQLdb.connect(host=conf.DB_HOST,user=conf.DB_USERNAEM,passwd=conf.DB_PASSWD,db=conf.DB_NAME,port=conf.DB_PORT,charset='utf8')
		cur=conn.cursor()
		cur.execute("select * from auth_user where username = '%s'"%username)
		result =  cur.fetchone(); 
		cur.close()
		conn.close()
		isExist = False
		try:
			user = User.objects.get(email=result[7])
			user.name = result[4]
			user.nickname = result[6].encode('utf8')
			user.save()
			isExist = True
		except (Exception) as e:
			isExist = False
			
		if isExist == False:
			user_pwd = stringToMD5(conf.PASSWD_FIXED_CHARACTER+result[4])
			user = User(name=result[4],
				         email= result[7],
				         nickname=result[6].encode('utf8'),
				         password=user_pwd,
				         create_time=getCurrentTime(),
				         edit_time=getCurrentTime(),
				         last_login_time = getCurrentTime(),
				         login_source = 1,
				         signin_source = 2,
				         signin_ip = '127.0.0.1',
				         userid='000000',
				         is_ctrip = 1,
				         )
			user.save()
		token = stringToMD5(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
		Token.save_token(token,result[7])
		resultInfo = {}
		resultInfo['token'] = token
		resultInfo['name'] = result[4]
		resultInfo['nickname'] = result[6].encode('utf8')
		resultInfo['email'] = result[7]
		resultDic.setResult(resultInfo)
	if fromSource == 'mobile':
		return resultDic.archiveJson()
	return resultDic.archiveJavaScript()
