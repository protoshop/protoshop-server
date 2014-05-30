# Python

## 返回数据格式

    ```javascript
    {
        "state":1, // state=0，是成功，message为空；state != 0,都是失败，message不为空；
        "message":"OK" //如果出现错误 这个字段会显示错误信息
        "code" : 1001
        "result":
        [
            结果(Result)
        ]
    }
    ```

## 模糊搜索用户列表

1. 接口地址：http://domain/ProtoShop/shareList/
2. 请求方式：GET、POST、JSON数据行
3. 请求参数：token appid keyword
4. 参数传送：无
5. 请求示例：无
6. 返回数据格式（JSON）：
    
     成功返回

    ```javascript
    {
        "result":[{"email": "kelixin@ctrip.com", "nickname": ""}, {"email": "lixinke@ctrip.com", "nickname": ""}, {"email": "xinkeli@ctrip.com", "nickname": ""}, {"email": "xkli@ctrip.com", "nickname": "xkli"}, {"email": "xkliy@ctrip.com", "nickname": ""}]}
        "status": "1" 
    }
    ```

    没有错误返回类型
webApp 解析此JSON 显示用



## 获取分享用户列表

1. 接口地址：http://domain/ProtoShop/sharelist/
2. 请求方式：GET
3. 请求参数：token
4. 参数传送：无
5. 请求示例：无
6. 返回数据格式（JSON）：
    
     成功返回

    ```javascript
    {
        "result":[{"email": "kelixin@ctrip.com", "nickname": ""}, {"email": "lixinke@ctrip.com", "nickname": ""}, {"email": "xinkeli@ctrip.com", "nickname": ""}, {"email": "xkli@ctrip.com", "nickname": "xkli"}, {"email": "xkliy@ctrip.com", "nickname": ""}]}
        "status": "1" 
    }
    ```

webApp 解析此JSON 显示用


## 分享工程

1. 接口地址：http://domain/ProtoShop/share/
2. 请求方式：POST
3. 请求参数：token appid user option (1添加 2删除) permission (1可读权限 2 可写权限)
4. 参数传送：如果单一用户直接传入  如果是多个用户传JSON 例：user {['user1','user2',....]}
5. 请求示例：无
6. 返回数据格式（JSON）：
    
    ```javascript
    {
        无
    }
    ```
webApp 解析此JSON 显示用


## iOS 注册推送token

1. 接口地址：http://domain/ProtoShop/registerdevice/
2. 请求方式：POST
3. 请求参数：token devicetoken
4. 参数传送：无
5. 请求示例：无
6. 返回数据格式（JSON）：
   
    
    ```javascript
    {
        无
    }
    ```
webApp 解析此JSON 显示用

## 意见反馈

1. 接口地址：http://domain/ProtoShop/feedback/
2. 请求方式：POST
3. 请求参数：toke|email（如果没有token必须要用户填写邮箱） content source(反馈来源 1：iOS 2:Andorid 3:webApp)
4. 参数传送：无
5. 请求示例：无
6. 返回数据格式（JSON）：

    ```javascript
    {
        无
    }
    ```

webApp 解析此JSON 显示用

## 修改密码

1. 接口地址：http://domain/ProtoShop/updatepwd/
2. 请求方式：POST
3. 请求参数：token passwd(需要MD5加密上传) oldpwd(需要MD5加密)
4. 参数传送：无
5. 请求示例：无
6. 返回数据格式（JSON）：
   
   修改成功
    
    ```javascript
    {
        "result": 
            {
                "email": "xxxxx@ctrip.com",
                "nickname": "xxxxx",
                "name":"xxxxx" （可以忽略此字段）
                "token": "",注：此token和发送这个服务所发送的token一样可以忽略
            }
     }
    ```
   
webApp 解析此JSON 显示用

## 用户登录接口

1. 接口地址：http://domain/ProtoShop/login/
2. 请求方式：POST
3. 请求参数：email passwd（32bit MD5之后的字符串）
4. 参数传送：无
5. 请求示例：无
6. 返回数据格式（JSON）：
   
   登录成功
    
    ```javascript
    {
        "result": 
            {
                "email": "xxxxx@ctrip.com",
                "nickname": "xxxxx",
                "name":"xxxxx" （可以忽略此字段）
                "token": "",注：此token和发送这个服务所发送的token一样可以忽略
            }, 
     }
    ```

webApp 解析此JSON 显示用


## 用户注册接口

1. 接口地址：http://domain/ProtoShop/register/
2. 请求方式：POST
3. 请求参数：email passwd nickname(可为空) username(可为空)
4. 参数传送：无
5. 请求示例：无
6. 返回数据格式（JSON）：
   
   注册成功
    
    ```javascript
    {
        "result": 
            {
                "email": "xxxxx@ctrip.com",
                "nickname": "xxxxx",
                "name":"xxxxx" （可以忽略此字段）
                "token": "",注：此token和发送这个服务所发送的token一样可以忽略
            }, 
     }
    ```
  
webApp 解析此JSON 显示用

## 获取用户信息接口

1. 接口地址：http://domain/ProtoShop/userinfo/
2. 请求方式：POST
3. 请求参数：token
4. 参数传送：无
5. 请求示例：无
6. 返回数据格式（JSON）：
   
   获取成功
    
    ```javascript
    {
        "result": 
            {
                "email": "xxxxx@ctrip.com", 
                "name": "xxxxx", 
                "nickname": "xxxxx"
            }, 
     }
    ```
   
webApp 解析此JSON 显示用

Enjoy.


## 更新用户信息接口

1. 接口地址：http://domain/ProtoShop/updateuser/
2. 请求方式：POST
3. 请求参数：token username(可为空) nickname(可为空)
4. 参数传送：无
5. 请求示例：无
6. 返回数据格式（JSON）：
    
    ```javascript
    {
        无
    }
    ```
webApp 解析此JSON 显示用

Enjoy.


## 获取工程列表接口（webApp使用接口）

1. 接口地址：http://domain/ProtoShop/fetchlist/
2. 请求方式：GET
3. 请求参数：device
4. 参数传送：token=xxx device=ios/android
5. 请求示例：http://domain/ProtoShop/fetchlist/?device=&token=xxx
6. 返回数据格式（JSON）：[/webapp/app/api/package/list.json](http://git.dev.sh.ctripcorp.com/wxd-pd/wxd-uitool/blob/master/webapp/app/api/package/list.json)  
7. JSON数据中'error_code'说明 10001 token为空 10002 token认证失败 10003 服务器内部错误（请反馈）
webApp 解析此JSON 显示用

Enjoy.


## 生成ZIP包

1. 请求地址：http://domain/ProtoShop/createZip/
2. 请求方式：POST
3. 请求参数：appid token
4. 返回结果（JSON格式）：
    成功：

    ```javascript
    {
        "url": "http://wxddb1.qa.nt.ctripcorp.com/packages/e6b472aa309546807fee70067769872b.zip",
    }
    ```
    "url"字段是下载zip包的链接,webApp拿到此URL即可下载ZIP包

    
5. 使用说明：
    App拿到服务端返回的数据 需要解析JSON 先看看 JSON的status字段
    如果status = "1" 则可以下载
    如果status = "0" 则生成zip包失败

Enjoy.


## 上传图片接口

1. 请求地址：http://domain/ProtoShop/uploadImage/
2. 请求方式：POST
3. 接口要求：发送请求时 appid以及图片的位置 不能修改，服务端暂时没有找到解决方案，找到解决方案后会把此要求删除
4. 请求参数：appid工程ID file图片文件 filename图片名字
5. 格式示例：appid='xxxxx' file=图片文件 filename如果第一次上传图片不需要填写 如果是覆盖以前的图片 需要上传现在的图片图片名字（带后缀）
    返回结果（JSON格式）：
    成功

    ```javascript
    {
        "appid": "317dbb3b28cc087dc15834d6b13e3bc7",
         "fileName": "", #有图片就传没有就传空 但是不能不传
    }
    ```

Enjoy.

## 创建工程接口

1. 请求地址：http://domain/ProtoShop/createPoject/
2. 请求方式：POST 
3. 请求参数：数据行 
4. 格式示例：appid='xxxxx' file=图片文件
   
    ```javascript
    {
         "context":
         {
            "token":"xxxxxxxxx"
            "appName":"tohell",
            "comment":"tohell 原型展示"
        }
     
    }
    ```
    

Enjoy.

## 删除工程

1. 接口地址：http://domain/ProtoShop/deleteProject/
2. 请求方式：GET
3. 请求参数：appid token
4. 返回数据格式（JSON)
4. 返回结果

    ```javascript
    {
        无
    }
    ```

Enjoy.

## 保存工程

1. 接口地址：http://domain/ProtoShop/saveProject/
2. 请求方式：POST
3. 请求参数：json格式

    ```javascript
    {
        "context": (在原来的基础上添加了一个token字段)
            {
                "token": "xxxxx",
                "appID": "xxxxx",
                "appDesc": "xxxxx"
                ......
            }, 
     }
    ```
4. 参数传送：无
5. 请求示例：无
6. 返回数据格式（JSON）： 

    ```javascript
    {
        无
    }
    ```

webApp 解析此JSON 显示用

Enjoy.

## 获取工程

1. 接口地址：http://domain/ProtoShop/fetchProject/
2. 请求方式：GET
3. 请求参数：appid token
4. 参数传送：无
5. 请求示例：无
6. 返回数据格式（JSON）：

    ```javascript
    {
       无
    }
    ```

webApp 解析此JSON 显示用

Enjoy.