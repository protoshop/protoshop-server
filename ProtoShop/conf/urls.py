# -*- coding:utf8 -*-
from django.conf.urls import patterns, include, url
from django_cas.views import login,logout  
from django.views.decorators.csrf import csrf_exempt
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))+'/api/')

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from ProtoShop.core.SSO.SSOAuth import SSOAuthCallBack
from ProtoShop.views.view import Hello as Welcome
import User
import ProtoShop.api.Projects as Projects
import ProtoShop.api.Share as Share
import ProtoShop.api.Mobile as Mobile
import ProtoShop.api.Feedback as Feedback
import ProtoShop.api.Search as Search
from ProtoShop.middleware.project.wsUploadImage import wsUploadImage # 上传图片

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ProtoShop.views.home', name='home'),
    # url(r'^ProtoShop/', include('ProtoShop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    
    ('^$',Welcome),
    ('^SSOAuthCallBack/$',SSOAuthCallBack),
    ('^SSOLogin/$', login),   
    ('^SSOLogout/$',logout),
    ('^login/$',User.login),
    ('^register/$',User.register),
    ('^userinfo/$',User.userInfo),                              #获取用户信息
    ('^updatepwd/$',User.updatepwd),                            #更新密码
    ('^updateuser/$',User.updateInfo),                          #更新用户信息
    ('^uploadImage/$',wsUploadImage),                            #上传图片接口
    ('^createZip/$',Mobile.wsCreateZip),                         #生成Zip包接口
    ('^fetchlist/$',Projects.wsFetchProjectList),                #获取工程列表接口
    ('^createPoject/$',Projects.wsCreateProject),                #创建工程接口
    ('^deleteProject/$',Projects.wsDeleteProject),               #删除工程接口
    ('^saveProject/$',Projects.wsSaveProject),                   #保存工程
    ('^fetchProject/$',Projects.wsFetchProject),                 # 获取工程配
    ('^feedback/$',Feedback.wsFeedBack),                         #意见反馈
    ('^registerdevice/$',Mobile.registToken),                    #注册token
    ('^share/$',Share.wsShareProject),
    ('^shareList/$',Share.wsShareList),
    ('^searchUser/$',Search.searchUser)
)
