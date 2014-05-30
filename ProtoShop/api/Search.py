from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ProtoShop.models.ProtoShop.models import User,ShareProject
from django.db.models import Q
import json
import ProtoShop.utils.token as Token
from ProtoShop.core.Package import Package

@csrf_exempt
def searchUser(request):
	resultDic = Package()
	resultDic.clear()
	keyword = ''
	appid = ''
	token = ''
	jsonStr = request.raw_post_data.decode('utf8')
	try:
		obj = json.loads(jsonStr)
		keyword = obj['keyword']
		appid = obj['appid']
		token = obj['token']
	except (Exception) as e:
		keyword =  request.GET.get('keyword')
		appid = request.GET.get('appid')
		token = request.GET.get('token')
		if not keyword:
			keyword =  request.POST.get('keyword')
			appid = request.POST.get('appid')
			token = request.POST.get('token')
	if keyword == '' or appid == '' or token =='':
		return HttpResponse('')
		
	userList = []
	if keyword == '@' or keyword == 'com' or keyword == 'cn' or keyword == '.' or keyword == 'org' or keyword == 'io' or keyword == 'me':
		resultDic.setResult(userList)
		return resultDic.archiveJson()
	users = User.objects.filter(email__contains=keyword)

	owner = ''
	if Token.check_token_isvalid(token):
			result = Token.get_token(token)
			owner = result.userName

	for x in range(len(users)):
		user = users[x]
		hasShare = ShareProject.objects.filter(share_ower=owner,share_user=user.email,appid=appid)
		if len(hasShare) <= 0:
			if owner == user.email:
				continue
			userDic = {}
			userDic['email'] = '%s'%user.email
			userDic['nickname'] = '%s'%user.nickname
			userList.append(userDic)
	resultDic.setResult(userList)
	return resultDic.archiveJson()
