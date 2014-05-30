# -*- coding:utf8 -*-
from UIKit import *
from CoreGraphics import *
import os
import codecs  
import json
import ProtoShop.conf.global_settings as CONFIG
# import ProtoShop.middleware.parser.wsFileUtil as fileUtil
#读取文件内容
def readFile(fileName):
	all_the_text = ''
	json_file = codecs.open(fileName,'r',"utf-8")
	try:
		all_the_text = json_file.read()
	finally:
		json_file.close()
	return all_the_text

def stringToColor(colorStr):
	if len(colorStr) < 7:
		return PSMakeColor(red=1.0,green=1.0,blue=1.0,alpha=1.0)
	red = float(int(colorStr[1:3],16))/255.0
	green = float(int(colorStr[3:5],16))/255.0
	blue = float(int(colorStr[5:7],16))/255.0
	color = PSMakeColor(red=red,green=green,blue=blue,alpha=1.0)
	return color

#获取字符串能力
def writeFile(fileName,text):
	file_object =  codecs.open(fileName, 'w',"utf-8")
	file_object.write(text.decode('utf8'))
	file_object.close()

PATCH_TEMPLATE_STR = 'require "indexViewController"\n\
indexViewController = indexViewController:init()\n\
local rootViewController = UIApplication:sharedApplication():keyWindow():rootViewController()\n\
rootViewController:pushViewController_animated(indexViewController, true)\n'

INDEXVIEWCONTROLLER_TEMPLATE_STR = 'waxClass{"indexViewController", wax.class[\'CTViewController\']}\n\
require "$requieName"\n\n\
function init(self)\n\
	self.super:init()\n\
  	return self\n\
end\n\
\n\
function viewDidLoad(self)\n\
	self.super:viewDidLoad()\n\
	self:navigationController():setNavigationBarHidden("YES")\n\
 	self:view():setBackgroundColor(UIColor:whiteColor())\n\
	self:loadViews()\n\
 end\n\
\n\
 function loadViews(self)\n\
 	local view = $ShowView:initWithFrame(self:view():bounds())\n\
	view:setDelegate(self)\n\
	self:view():addSubview(view)\n\
 end\n\n'


SCENE_TEMPLATE_STR = 'waxClass{"$className", wax.class[\'CTView\']}\n\
$requieName\n\n\
function initWithFrame(self)\n\
	self.super:initWithFrame(frame)\n\
	self:loadViews()\n\
  	return self\n\
end\n\
\n\
 function loadViews(self)\n\
 	local documentsDirectory = NSDocumentDirectory\n\
  	local imagePath = documentsDirectory.."/$userName/$appid/" \n\
  	self:setBackgroundImage(imagePath.."$bgimageName")\n\
    $subViews\n\
 end\n\
 \n\
 \n$functions\n'

def createFrame(info):
	frame = PSMakeFrame(float(info['posX']),float(info['posY']),float(info['width']),float(info['height']))
	return frame
def createColor(info):
	color = PSMakeColor(float(info['bkColorRed']),float(info['bkColorGreen']),float(info['bkColorBlue']),float(info['bkAlpha']))
	return color

def addButtonClickAction(actionList):
	actionStr = ''
	for x in range(len(actionList)):
		actionInfo = actionList[x]


def handlerButton(superView,buttonInfo):
	frame = createFrame(buttonInfo)
	button = PSButton(frame)
	button.title = buttonInfo['text']
	if buttonInfo.has_key('bgColor'):
		button.bgcolor = stringToColor(buttonInfo['bgColor'])
	if buttonInfo.has_key('textSize'):
		button.fontSize = buttonInfo['textSize']
	if buttonInfo.has_key('textColor'):
		button.titleColor = stringToColor(buttonInfo['textColor'])

	requireStr = ''
	subViewStr = ''
	functionStr = ''
	if buttonInfo.has_key('elements'):
		elementsList = buttonInfo['elements']
		if len(elementsList) > 0:
			requireStr,subViewStr,functionStr = loadElements(button.name,elementsList)

	actionList = []
	actionInfoDic = buttonInfo['jumpto']
	actionList.append(actionInfoDic)
	isAction = False
	if len(actionList) > 0:
		actionInfo = actionList[0]
		if len(actionInfo['target'])>0 and actionInfo['target'] != None:
			button.actionName = 'goto%s'%str(actionInfo['target'])
			button.targetName = 'view%s'%str(actionInfo['target'])

			transition = 0
			direction = 0
			duration = '%f'%actionInfo['transitionDuration']
			transitionStr = actionInfo['transitionType']
			if transitionStr =='push':
				transition = 1
			elif transitionStr =='cover':
				transition = 2
			else :
				transition = 0
		
			directionStr = actionInfo['transitionDirection']
			if directionStr =='left':
				direction = 1
			if directionStr =='right':
				direction = 2
			if directionStr =='up':
				direction = 3
			if directionStr =='down':
				direction = 4
			button.actionTransition = transition
			button.actionDirection = direction
			button.actionDuration = duration
			functionStr = button.addClickAction(str(actionInfo['target']))
			requireStr = 'require "%s"\n'%button.targetName
			isAction = True
		else:
			isAction = False
	return button.CreateLua(superView,isAction) + subViewStr,functionStr,requireStr

def handlerLabel(superView,labelInfo):
	frame =createFrame(labelInfo)
	label = PSLabel(frame)
	label.text = str(labelInfo['text'].encode('utf8'))
	label.fontSize = int(labelInfo['textSize'])
	label.textColor = stringToColor(labelInfo['textColor']) 
	'''
	这两个属性暂时不支持
	'''
	
	# label.bgColor =  createColor(labelInfo['bgColor'])
	# label.alignment = int(labelInfo['alignment'])
	
	requireStr = ''
	subViewStr = ''
	functionStr = ''

	if labelInfo.has_key('elements'):
		elementsList = labelInfo['elements']
		if len(elementsList) > 0:
			requireStr,subViewStr,functionStr = loadElements(label.name,elementsList)
	return label.CreateLua(superView) + subViewStr,functionStr,requireStr

def handlerImageView(superView,imageViewInfo):
	frame = createFrame(imageViewInfo)
	imageView = PSImageView(frame,str(imageViewInfo['image']))
	requireStr = ''
	subViewStr = ''
	functionStr = ''
	if imageViewInfo.has_key('elements'):
		elementsList = imageViewInfo['elements']
		if len(elementsList) > 0:
			requireStr,subViewStr,functionStr = loadElements(imageView.name,elementsList)
	return imageView.CreateLua(superView) + subViewStr,functionStr,requireStr


def handlerView(superView,viewInfo):
	frame = createFrame(viewInfo)
	view = PSView(frame)
	view.bgcolor = stringToColor(viewInfo['bgColor'])

	requireStr = ''
	subViewStr = ''
	functionStr = ''

	if viewInfo.has_key('elements'):
		elementsList = viewInfo['elements']
		if len(elementsList) > 0:
			requireStr,subViewStr,functionStr = loadElements(view.name,elementsList)
	return view.CreateLua(superView) + subViewStr,functionStr,requireStr

def handlerScrollView(superView,scrollInfo):
	frame = createFrame(scrollInfo)
	scrollView = PSScrollView(frame)
	scrollView.bgcolor = stringToColor(scrollInfo['bgColor'])
	anchorOriginX = 0;
	anchorOriginY = 0;
	if scrollInfo.has_key('contentOffset'):
		anchorOriginX = float(scrollInfo['contentOffset']['anchorOriginX'])
		anchorOriginY = float(scrollInfo['contentOffset']['anchorOriginY'])
	scrollView.contentOffSet = PSMakeContentOffSet(anchorOriginX,anchorOriginY)
	scrollView.contentSize = PSMakeContentSize(float(scrollInfo['contentSize']['width']),float(scrollInfo['contentSize']['height']))
	
	requireStr = ''
	subViewStr = ''
	functionStr = ''

	if scrollInfo.has_key('elements'):
		elementsList = scrollInfo['elements']
		if len(elementsList) > 0:
			requireStr,subViewStr,functionStr = loadElements(scrollView.name,elementsList)
	return scrollView.CreateLua(superView) + subViewStr,functionStr,requireStr
	

def loadElements(superView,elementsList):
	requireStr = ''
	functionStr = ''
	subViewStr = ''
	for x in range(len(elementsList)):
		elementObj = elementsList[x]
		elementType = elementObj['type']

		if elementType == 'scrollview':
			tmpView,tmpAction,tmpRequire = handlerScrollView(superView,elementObj)
			subViewStr = subViewStr + tmpView
			requireStr = tmpRequire + requireStr
			functionStr = functionStr + tmpAction
		elif elementType == 'label':
			tmpView,tmpAction,tmpRequire =  handlerLabel(superView,elementObj)
			subViewStr = subViewStr + tmpView
			requireStr = tmpRequire + requireStr
			functionStr = functionStr + tmpAction
		elif elementType == 'button':
			tmpView,tmpAction,tmpRequire = handlerButton(superView,elementObj)
			subViewStr = subViewStr + tmpView
			requireStr = tmpRequire + requireStr
			functionStr = functionStr + tmpAction
		elif elementType == 'imageview':
			tmpView,tmpAction,tmpRequire = handlerImageView(superView,elementObj)
			subViewStr = subViewStr + tmpView
			requireStr = tmpRequire + requireStr
			functionStr = functionStr + tmpAction
		elif elementType == 'view':
			tmpView,tmpAction,tmpRequire = handlerView(superView,elementObj)
			subViewStr = subViewStr + tmpView
			requireStr = tmpRequire + requireStr
			functionStr = functionStr + tmpAction
		else:
			pass
	return requireStr,subViewStr,functionStr

def feed(userName,projectObj):
	try:
		appid = str(projectObj['appID'])
		protjectScences = projectObj['scenes']
		indexScenceName = ''
		for x in range(len(protjectScences)):
			scenceObj = protjectScences[x]
			if int(scenceObj['order']) == 0:
				indexScenceName = 'view%s'%str(scenceObj['id'])
			scenceName = 'view%s'%str(scenceObj['id'])
			scenceStr = SCENE_TEMPLATE_STR
			requireStr,subViewStr,functionStr = loadElements('self',scenceObj['elements'])
			requireList = list(set(requireStr.split('\n')))
			requireResultStr = ''
			for x in range(len(requireList)):
				tmpStr = str(requireList[x])
				if len(tmpStr) > 0:
					requireResultStr = requireResultStr + tmpStr +'\n'

			
			scenceStr = scenceStr.replace('$bgimageName',str(scenceObj['background']))
			scenceStr = scenceStr.replace('$className',scenceName)
			scenceStr = scenceStr.replace('$requieName',requireResultStr)
			scenceStr = scenceStr.replace('$subViews',subViewStr)
			scenceStr = scenceStr.replace('$functions',functionStr)
			scenceStr = scenceStr.replace('$userName',userName)
			scenceStr = scenceStr.replace('$appid',appid)

			writeFile(CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH+appid+'/'+scenceName+'.lua',scenceStr)
		indexVCStr = INDEXVIEWCONTROLLER_TEMPLATE_STR
		indexVCStr = indexVCStr.replace('$requieName',indexScenceName)
		indexVCStr = indexVCStr.replace('$ShowView',indexScenceName)
		writeFile(CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH+'/'+appid+'/indexViewController.lua',indexVCStr)
		writeFile(CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH+'/'+appid+'/patch.lua',PATCH_TEMPLATE_STR)
		return 1
	except Exception, e:
		return str(e)
	
if __name__ == '__main__':
	print feed('fkzhao@ctrip.com','2e4626f39628940f7928e2bf0ce186f5')