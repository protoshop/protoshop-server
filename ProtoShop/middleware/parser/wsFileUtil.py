# -*- coding: utf-8 -*-
import os
import codecs  
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
	file_object.write(text)
	file_object.close()
