# -*- coding:utf-8 -*-	
from django.db import models
 
class User(models.Model): 
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32,default='')
    nickname = models.CharField(max_length=32,default='')
    email = models.CharField(null=True,max_length=50)
    password = models.CharField(null=True,max_length=32)
    create_time = models.CharField(max_length=30,default='')
    edit_time = models.CharField(max_length=30,default='')
    last_login_time = models.CharField(max_length=30,default='')
    login_source = models.IntegerField(default= 1)
    signin_source = models.IntegerField(default=1)
    is_ctrip = models.IntegerField(default=1)
    signin_ip = models.CharField(max_length=20,default='')
    userid = models.IntegerField(default=1)

class Projects(models.Model): 
    id = models.AutoField(primary_key=True)
    appid = models.CharField(null=True,max_length=40)
    description = models.CharField(null=True,max_length=200)
    name = models.CharField(null=True,max_length=40)
    icon = models.CharField(max_length=100)
    platform = models.IntegerField()# 1 iOS  2 Android
    create_time = models.CharField(max_length=20)
    edit_time = models.CharField(max_length=20)
    public = models.IntegerField()# 1 private 2 public
    path = models.CharField(max_length=100)
    owner = models.CharField(null=True,max_length=20)

  
class ShareProject(models.Model): 
    id = models.AutoField(primary_key=True)
    appid = models.CharField(null=True,max_length=40)
    share_user = models.CharField(null=True,max_length=30)
    share_time = models.CharField(max_length=20)
    share_ower = models.CharField(null=True,max_length=30)
    permission = models.IntegerField(default=1)# 1:可读 2:可写(拥有所有权限)


  
class Token(models.Model): 
    id = models.CharField(max_length=20)
    access_token = models.CharField(primary_key=True,max_length=40)
    create_time = models.CharField(max_length=20)
    end_time = models.CharField(max_length=20)
    token_source = models.CharField(max_length=20)
    token_apply_ip = models.CharField(max_length=20)

class Feedback(models.Model): 
    user_name =models.CharField(null=True,max_length=30)
    content = models.CharField(null=True,max_length=256)
    create_time = models.CharField(max_length=20)
    source = models.IntegerField()#1:iOS 2:Android 3:webApp

class DeviceToken(models.Model): 
    user_name = models.CharField(null=True,max_length=30)
    device_token = models.CharField(null=True,max_length=50)
    device_ip = models.CharField(max_length=20)
    last_time = models.CharField(max_length=20)
