# -*- coding:utf8 -*-
import os
import codecs  
import json
import uuid
import sys
import ProtoShop.conf.global_settings as CONFIG

reload(sys)
sys.setdefaultencoding("utf-8")

SCENCE_TEMPLATE_STR = 'Command = luajava.bindClass("com.protoshop.lua.Command")\n\
function onCreate( activity )\n\
	#scence=Command:createScence(activity,"#appID", "#backgroud")\n\
	#addView\n\
end\n\
\n\
--程序再次进入\n\
function onResume( activity )\
end\
\n\
--程序进入后台\n\
function onStop( activity )\
end\n'

CREATE_VIEW_TEMPLATE_STR = '#view=Command:createView(activity,\'#type\')\n'

SET_ATTRIBUTE_TEMPLATE_STR = 'Command:setAttr(#parent,#view,\'#attrJson\',\'#lable\')\n '

SET_ACTION_TEMPLATE_STR = 'Command:setAction(#view,\'#actionJson\')\n'


#读取文件内容
def readFile(fileName):
	all_the_text = ''
	json_file = codecs.open(fileName,'r',"utf-8")
	try:
		all_the_text = json_file.read()
	finally:
		json_file.close()
	return all_the_text

#获取字符串能力
def writeFile(fileName,text):
	file_object =  codecs.open(fileName, 'w',"utf-8")
	file_object.write(text.decode('utf8'))
	file_object.close()

def createViewID(elementObject):
	uuidStr = str(uuid.uuid4())
	uuidStr = uuidStr.replace('-','')
	result = "id" + str(elementObject['type']) + uuidStr + str(elementObject['posX'])+ str(elementObject['posY'])+ str(elementObject['width'])+ str(elementObject['height'])
	return result

def checkDirection(elementObject):
	width = float(elementObject['width'])
	height = float(elementObject['height'])
	contentwidth = float(elementObject['contentSize']['width'])
	contentheight = float(elementObject['contentSize']['height'])
	
	cofwith = contentwidth / width
	cofhight = contentheight /height
	if cofwith > cofhight:
		return 'horizontal'
	elif cofwith == cofhight:
		return 'vertical'
	else:
		return 'vertical'

def parseElements(parentID, parentElementObject, createViewTemplate, setAttrTemplate,setActionTemplate):
	elementBuffer = ''

	elementArray = []
	if parentElementObject.has_key('elements'):
		elementArray = parentElementObject['elements']
	
	if not isinstance(elementArray,list):
		return elementBuffer

	for x in range(len(elementArray)):
		createViewStr = createViewTemplate
		setAttrStr = setAttrTemplate
		elementObject = elementArray[x];
		viewType = str(elementObject['type'])
		
		viewId = createViewID(elementObject)
		
		createViewStr = createViewStr.replace('#type',viewType)
		createViewStr = createViewStr.replace('#view',viewId)
		elementBuffer = elementBuffer + createViewStr + '\n'
		if viewType == 'scrollview':
			elementObject['orientation'] = checkDirection(elementObject)
		setAttrStr = setAttrStr.replace('#attrJson',json.dumps(elementObject, encoding='utf-8'))
		setAttrStr = setAttrStr.replace('#view',viewId)
		setAttrStr = setAttrStr.replace('#parent',str(parentID))
		if viewType=='label' or viewType == 'button':
			text= str(elementObject['text'])
			setAttrStr= setAttrStr.replace('#lable',str(text))
		else:
			setAttrStr= setAttrStr.replace('#lable','')
			

		elementBuffer = elementBuffer + setAttrStr + '\n'

		elementBuffer = elementBuffer + parseElements(viewId,elementObject,createViewTemplate, setAttrTemplate, setActionTemplate)

		if elementObject.has_key('jumpto'):
			actionArray = []
			actionInfoDic = elementObject['jumpto']
			actionArray.append(actionInfoDic)
			for y in range(len(actionArray)):
				actionObject = actionArray[y]
				setActionStr = setActionTemplate
				setActionStr = setActionStr.replace('#actionJson',json.dumps(actionObject,encoding='utf-8'))
				setActionStr = setActionStr.replace('#view',viewId)
				elementBuffer = elementBuffer + setActionStr + '\n'

	elementBuffer = elementBuffer + '\n'
	return elementBuffer

def feed(userName,projectObj):
	try:
		appid = str(projectObj['appID'])
		scenceArray = projectObj['scenes']
		home_scence = ''
		for x in range(len(scenceArray)):
			scenceStr = SCENCE_TEMPLATE_STR
			scenceStr = scenceStr.replace('#appID',appid)
			scenceObj = scenceArray[x]
			scenceId = str(scenceObj['id'])
			order = str(scenceObj['order'])
			if order == '0':
				home_scence = scenceId
			background = str(scenceObj['background'])
			scenceStr = scenceStr.replace('#backgroud',background)
			scenceStr = scenceStr.replace("#scence",'id' + scenceId)
			createViewTemplate = CREATE_VIEW_TEMPLATE_STR
			setAttrTemplate = SET_ATTRIBUTE_TEMPLATE_STR
			setActionTemplate = SET_ACTION_TEMPLATE_STR

			elementStr = parseElements("id" + scenceId, scenceObj, createViewTemplate, setAttrTemplate,setActionTemplate);

			scenceStr = scenceStr.replace('#addView',elementStr)
			scenceStr = scenceStr.replace('#','$')
			writeFile(CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH+appid+'/'+scenceId+'.lua',scenceStr)

		writeFile(CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH+appid+'/patch.lua',home_scence)
		return 1
	except Exception, e:
		return 0
	



if __name__ == '__main__':
	print feed('fkzhao@ctrip.com','2e4626f39628940f7928e2bf0ce186f5')

