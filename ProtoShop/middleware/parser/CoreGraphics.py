# -*- coding: utf-8 -*-


class PSFrame(object):
	"""docstring for PSFrame"""
	def __init__(self, originX=0.0,originY=0.0,width=0.0,height=0.0):
		super(PSFrame, self).__init__()
		self.originX = originX
		self.originY = originY
		self.width = width
		self.height = height

class PSColor(object):
	"""docstring for PSColor"""
	def __init__(self, red=0.0,green=0.0,blue=0.0,alpha=0.0):
		super(PSColor, self).__init__()
		self.red = red
		self.green = green
		self.blue = blue
		self.alpha = alpha

class PSContentOffSet(object):
	"""docstring for PSContentOffSet"""
	def __init__(self, originX=0.0,originY=0.0):
		super(PSContentOffSet, self).__init__()
		self.originX = originX
		self.originY = originY
		
class PSContentSize(object):
	"""docstring for PSContentSize"""
	def __init__(self, width = 0.0,height = 0.0):
		super(PSContentSize, self).__init__()
		self.width = width
		self.height = height
		

def PSMakeFrame(originX=0.0,originY=0.0,width=0.0,height=0.0):
	"""Make Frame"""
	frame = PSFrame(originX=originX,originY=originY,width=width,height=height)
	return frame


def PSMakeColor(red=0.0,green=0.0,blue=0.0,alpha=1.0):
	"""Make Color"""
	color = PSColor(red=red,green=green,blue=blue,alpha=alpha)
	return color

def PSMakeContentOffSet(originX=0.0,originY=0.0):
	"""Make ContentOffSet"""
	contentOffSet = PSContentOffSet(originX=originX,originY=originY)
	return contentOffSet

def PSMakeContentSize(width = 0.0,height = 0.0):
	"""Make ContentSize"""
	contentSize = PSContentSize(width=width,height=height)
	return contentSize


