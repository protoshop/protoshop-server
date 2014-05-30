# -*- coding:utf8 -*-
'''
全局配置文件(Global Configuration)
'''


'''
Django开发模式配置 (Development Mode Configuration)
'''
DEBUG = True

'''
开发模式配置 (Development Mode Configuration)
'''

IS_DEBUG = False
'''
服务器配置 (Development Mode Configuration)
'''
IS_PROTOSHOP_IO = True

'''
数据库相关配置 (Database Configuration)
'''
DB_TYPE = 'mysql'
DB_USERNAEM = 'xxxx'
DB_PASSWD = '*****'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = ''


'''
SSO 认证配置 (SSO Auth Configuration)
'''
SSO_AUTH_URL = ''
SSO_REDIRECT_URL = 'url'


'''
密码验证配置 (Password Authentication Configuration)
'''
#token有效时间(单位s)
MAX_TOKEN_EFFECTIVE_TIME = 时间 
PASSWD_FIXED_CHARACTER = 'ProtoShop'


'''
模板文件路径配置&存放Lua文件路径配置(Save Path Configuration)
'''
LUA_TEMPLATE_FILE_IOS_DIR = ''
LUA_TEMPLATE_FILE_ANDROID_DIR = ''
WRITE_LUA_SCRIPT_FILE_BASE_PATH = ''
PROJECT_FILE_PATH = ''
PROJECT_ICON_URL = ''
PROJECT_DOWNLOAD_URL = ''


if IS_DEBUG :
	DB_NAME = 'ProtoShop_test'
	SSO_AUTH_URL = '****'
else :
	DB_NAME = 'ProtoShop'
	SSO_AUTH_URL = '****'

if IS_PROTOSHOP_IO:
    PROJECT_DOWNLOAD_URL = 'http://domain/packages/'
else :
    PROJECT_DOWNLOAD_URL = 'http://domain/packages/'

if IS_DEBUG :
    WRITE_LUA_SCRIPT_FILE_BASE_PATH ='Absolute path'
    PROJECT_FILE_PATH = 'Absolute path/projectList.json'
    PROJECT_ICON_URL = 'http://domain/packages/icon.png'
    
else :
    WRITE_LUA_SCRIPT_FILE_BASE_PATH ='Absolute path'
    PROJECT_FILE_PATH = 'Absolute path/projectList.json'
    PROJECT_ICON_URL = 'http://domain/packages/icon.png'
    PROJECT_DOWNLOAD_URL = 'http://domain/packages/'


'''
Redis 配置
'''

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 1


	




