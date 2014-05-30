# -*- coding: utf-8 -*-
from CoreGraphics import *

class PSView(object):
	"""docstring for PSView"""

	def __init__(self, frame):
		super(PSView, self).__init__()
		self.name = 'baseView'
		self.frame = frame
		self.bgcolor = PSMakeColor(red=1.0, green=1.0, blue=1.0, alpha=0.0)
		self.viewTemplateStr = '	$viewlNameDic = {}\n\
	$viewNameDic["frame"] = {originX = $startX,originY = $startY,sizeWidth = $width,sizeHeight = $hight}\n\
	$viewNameDic["bkColor"] = {bkColorRed = $red,bkColorGreen = $green,bkColorBlue = $blue,bkAlpha = $alpha}\n\
	local $viewlName = self:command_createView($superView,$info)\n'
		self.luaString = ''

	def CreateLua(self,superView):
		baseStr = self.viewTemplateStr
		baseStr = baseStr.replace('$viewName',self.name)
		baseStr = baseStr.replace('$startX',str(self.frame.originX))
		baseStr = baseStr.replace('$startY',str(self.frame.originY))
		baseStr = baseStr.replace('$width',str(self.frame.width))
		baseStr = baseStr.replace('$hight',str(self.frame.height))

		baseStr = baseStr.replace('$red',str(self.bgcolor.red))
		baseStr = baseStr.replace('$green',str(self.bgcolor.green))
		baseStr = baseStr.replace('$blue',str(self.bgcolor.blue))
		baseStr = baseStr.replace('$alpha',str(self.bgcolor.alpha))

		baseStr = baseStr.replace('$viewlName',self.name)
		baseStr = baseStr.replace('$superView',superView)
		baseStr = baseStr.replace('$info',self.name+'Dic')

		self.luaString = baseStr
		return self.luaString


class PSLabel(PSView):
	"""docstring for PSLabel"""
	
	testName = 2
	def __init__(self, frame):
		super(PSLabel, self).__init__(frame)
		self.name = 'label'+'_%d%d%d%d'%(int(self.frame.originX),int(self.frame.originY),int(self.frame.width),int(self.frame.height))
		self.text = ''
		self.alignment = 0
		self.fontSize = 15
		self.bgColor = PSMakeColor()
		self.textColor = PSMakeColor()
		self.labelTemplateStr = '	$labelNameDic["textInfo"] = {fontName = "$fontName",fontSize = $fontSize,text = "$text",textColor =\
	{textColorRed = $red,textColorGreen = $green,textColorBlue = $blue,textAlpha = $alpha},alignment = $alignment}\n\
	local $labelName = self:command_createLabel($superView,$info)\n'

	def CreateLua(self,superView):
		baseStr =  super(PSLabel,self).CreateLua(superView)
		labelStr = self.labelTemplateStr

		labelStr = labelStr.replace('$red',str(self.textColor.red))
		labelStr = labelStr.replace('$green',str(self.textColor.green))
		labelStr = labelStr.replace('$blue',str(self.textColor.blue))
		labelStr = labelStr.replace('$alpha',str(self.textColor.alpha))

		labelStr = labelStr.replace('$fontName','System')
		labelStr = labelStr.replace('$fontSize',str(self.fontSize))
		labelStr = labelStr.replace('$alignment',str(self.alignment))
		labelStr = labelStr.replace('$text',str(self.text))

		labelStr = labelStr.replace('$labelName',self.name)
		labelStr = labelStr.replace('$superView',superView)
		labelStr = labelStr.replace('$info',self.name+'Dic')

		self.luaString = baseStr + labelStr
		return self.luaString


class PSImageView(PSView):
	"""docstring for PSImageView"""
	def __init__(self, frame,imageName):
		super(PSImageView, self).__init__(frame)
		self.name = 'imageView'+'_%d%d%d%d'%(int(self.frame.originX),int(self.frame.originY),int(self.frame.width),int(self.frame.height))
		self.imageName = imageName
		self.imageTemplateStr = '	$imageViewDic["imageName"] = imagePath.."$imageName"\n\
	local $imageView = self:command_createImageview($superView,$info)\n'

	def CreateLua(self,superView):
		baseStr =  super(PSImageView,self).CreateLua(superView)
		imageViewStr = self.imageTemplateStr

		imageViewStr = imageViewStr.replace('$imageView',self.name)
		imageViewStr = imageViewStr.replace('$superView',superView)
		imageViewStr = imageViewStr.replace('$imageName',self.imageName)
		imageViewStr = imageViewStr.replace('$info',self.name+'Dic')

		self.luaString = baseStr + imageViewStr
		return self.luaString


class PSButton(PSView):
	"""docstring for PSButton"""

	def __init__(self, frame):
		super(PSButton, self).__init__(frame)
		self.name = 'btn'+'_%d%d%d%d'%(int(self.frame.originX),int(self.frame.originY),int(self.frame.width),int(self.frame.height))
		self.title = 'button'
		self.actionStr = ''
		self.actionName = 'action'+'_%d%d%d%d'%(int(self.frame.originX),int(self.frame.originY),int(self.frame.width),int(self.frame.height))
		self.titleColor = PSMakeColor()
		self.targetName = ''
		self.fontSize = 16
		self.actionTransition = 1
		self.actionDirection = 2
		self.actionDuration = 0.25
		self.buttonTemplateStr = '	$buttonNameDic["titleInfo"] = {\n\
	titleText = "$buttonTitle",controlState = 0,fontSize = $fontSize,alignment = 0,titleColor={titleColorRed = $red,titleColorGreen = $green,titleColorBlue = $blue,titleAlpha = $alpha}}\n\
	local btn = self:command_createBtn($superView,$info)\n\
	self:addEvent_event(btn,"$buttonAction")\n'

		self.actionTemplateStr = 'function $actionName(self,sender)\n\
	local view = $targetName:initWithFrame(self:bounds())\n\
	view:setDelegate(self:delegate())\n\
	self:clickAction_animatType_direction_delayTime(view,$transition,$direction,$duration)\n\
end\n\n'
	
	def __setter__(self, obj, val):
	 	print ''

	def addClickAction(self,target):
		actionName = self.actionName + '%d%d%d%d'%(int(self.frame.originX),int(self.frame.originY),int(self.frame.width),int(self.frame.height))
		actionStr = self.actionTemplateStr
		actionStr = actionStr.replace('$actionName',str(actionName))
		actionStr = actionStr.replace('$targetName',str(self.targetName))
		actionStr = actionStr.replace('$transition',str(self.actionTransition))
		actionStr = actionStr.replace('$direction',str(self.actionDirection))
		actionStr = actionStr.replace('$duration',str(self.actionDuration))

		self.actionStr = actionStr
		return self.actionStr

	def CreateLua(self,superView,hasAction):
		baseStr = super(PSButton,self).CreateLua(superView)
		if hasAction:
			actionName = self.actionName + '%d%d%d%d'%(int(self.frame.originX),int(self.frame.originY),int(self.frame.width),int(self.frame.height))
		else:
			actionName = ''
		buttonStr = self.buttonTemplateStr
		buttonStr = buttonStr.replace('$buttonName',str(self.name))
		buttonStr = buttonStr.replace('$buttonTitle',str(self.title))
		buttonStr = buttonStr.replace('$fontSize',str(self.fontSize))

		buttonStr = buttonStr.replace('$red',str(self.titleColor.red))
		buttonStr = buttonStr.replace('$green',str(self.titleColor.green))
		buttonStr = buttonStr.replace('$blue',str(self.titleColor.blue))
		buttonStr = buttonStr.replace('$alpha',str(self.titleColor.alpha))

		buttonStr = buttonStr.replace('$buttonAction',actionName)
		buttonStr = buttonStr.replace('$superView',superView)
		buttonStr = buttonStr.replace('$info',self.name+'Dic')

		self.luaString = baseStr +  buttonStr
		return self.luaString


class PSScrollView(PSView):
	"""docstring for PSScrollView"""
	def __init__(self, frame):
		super(PSScrollView, self).__init__(frame)
		self.name = 'scrollView'+'_%d%d%d%d'%(int(self.frame.originX),int(self.frame.originY),int(self.frame.width),int(self.frame.height))
		self.contentOffSet = PSMakeContentOffSet()
		self.contentSize = PSMakeContentSize()
		self.scrollTemplateStr = '	$scrollNameDic["contentOffset"] = {anchorOriginX = $anchorOriginX,anchorOriginY = $anchorOriginY}\n\
	$scrollNameDic["contentSize"] = {contentSizeWidth = $contentSizeWidth,contentSizeHeight = $contentSizeHeight}\n\
	local $scrollName = self:command_createScrollView($superView,$info)\n'
	
	def CreateLua(self,superView):
		baseStr = super(PSScrollView,self).CreateLua(superView)
		scrollStr = self.scrollTemplateStr

		scrollStr = scrollStr.replace('$anchorOriginX',str(self.contentOffSet.originX))
		scrollStr = scrollStr.replace('$anchorOriginY',str(self.contentOffSet.originY))
		scrollStr = scrollStr.replace('$contentSizeWidth',str(self.contentSize.width))
		scrollStr = scrollStr.replace('$contentSizeHeight',str(self.contentSize.height))

		scrollStr = scrollStr.replace('$scrollName',self.name)
		scrollStr = scrollStr.replace('$superView',superView)
		scrollStr = scrollStr.replace('$info',self.name+'Dic')

		self.luaString = baseStr +  scrollStr
		return self.luaString






