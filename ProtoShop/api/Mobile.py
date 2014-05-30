# -*- coding:utf8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import zipfile
import os
import json
import ProtoShop.conf.global_settings as CONFIG
import ProtoShop.middleware.parser.wsParser as Parser
import ProtoShop.utils.token as Token
from ProtoShop.core.Package import Package

def zipdir(dirPath=None, zipFilePath=None, includeDirInZip=True):
    """Create a zip archive from a directory.
    
    Note that this function is designed to put files in the zip archive with
    either no parent directory or just one parent directory, so it will trim any
    leading directories in the filesystem paths and not include them inside the
    zip archive paths. This is generally the case when you want to just take a
    directory and make it into a zip file that can be extracted in different
    locations. 
    
    Keyword arguments:
    
    dirPath -- string path to the directory to archive. This is the only
    required argument. It can be absolute or relative, but only one or zero
    leading directories will be included in the zip archive.

    zipFilePath -- string path to the output zip file. This can be an absolute
    or relative path. If the zip file already exists, it will be updated. If
    not, it will be created. If you want to replace it from scratch, delete it
    prior to calling this function. (default is computed as dirPath + ".zip")

    includeDirInZip -- boolean indicating whether the top level directory should
    be included in the archive or omitted. (default True)

"""
    if not zipFilePath:
        zipFilePath = dirPath + ".zip"
    if not os.path.isdir(dirPath):
        raise OSError("dirPath argument must point to a directory. "
            "'%s' does not." % dirPath)
    parentDir, dirToZip = os.path.split(dirPath)
    #Little nested function to prepare the proper archive path
    def trimPath(path):
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            archivePath = archivePath.replace(os.path.sep, "", 1)
        if not includeDirInZip:
            archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)
        return os.path.normcase(archivePath)
        
    outFile = zipfile.ZipFile(zipFilePath, "w",
        compression=zipfile.ZIP_DEFLATED)
    for (archiveDirPath, dirNames, fileNames) in os.walk(dirPath):
        for fileName in fileNames:
            filePath = os.path.join(archiveDirPath, fileName)
            outFile.write(filePath, trimPath(filePath))
        #Make sure we get empty directories as well
        if not fileNames and not dirNames:
            zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
            #some web sites suggest doing
            #zipInfo.external_attr = 16
            #or
            #zipInfo.external_attr = 48
            #Here to allow for inserting an empty directory.  Still TBD/TODO.
            outFile.writestr(zipInfo, "")
    outFile.close()


@csrf_exempt
def wsCreateZip(request):
	#返回给前端的
    resultDic = Package()
    resultDic.clear()
	#获取JSON
    appid = ''
    token = ''
    if request.POST:
        appid = request.POST.get('appid','')
        token = request.POST.get('token','')
    else:
        appid = request.GET.get('appid','')
        token = request.GET.get('token','')

    if not Token.check_token_isvalid(token):
        resultDic.status = 1
        resultDic.code = 15004
        resultDic.message = 'toke失效 请重新登录'

    userName = ''
    result = Token.get_token(token)
    userName = result.userName

    try:
        flag = Parser.wsParser(appid,userName)
        if (flag == 1):
            target_dir = CONFIG.WRITE_LUA_SCRIPT_FILE_BASE_PATH
            target = target_dir + appid + '.zip'
            if (os.path.exists(target_dir + appid)):
                zipdir(target_dir + appid,target)
                downloadUrl = CONFIG.PROJECT_DOWNLOAD_URL + appid + '.zip'
                resultDictory = {}
                resultDictory['url'] = downloadUrl
                resultDic.setResult(resultDictory)
            else:
                resultDic.status = 1
                resultDic.code = 15002
                resultDic.message = '服务器内部异常'
        else:
            resultDic.status = 1
            resultDic.code = 15003
            resultDic.message = flag#'Lua解析失败'

    except (Exception) as e:
        resultDic.status = 1
        resultDic.code = 15005
        resultDic.message = 'Lua解析异常'

    return resultDic.archiveJson()

@csrf_exempt
def registToken(request):
    from ProtoShop.models.ProtoShop.models import DeviceToken
    resultDic = Package()
    resultDic.clear()
    if request.POST:
        token = request.POST.get('token','')
        devicetoken = request.POST.get('devicetoken','')
        if devicetoken == '':
            resultDic.status = 1
            resultDic.code = 14002
            resultDic.message = 'deviceToken为空'
        else:
            import ProtoShop.utils.token as Token
            from ProtoShop.utils.views import getCurrentTime,getIP
            if Token.check_token_isvalid(token):
                try:
                    userName = ''
                    result = Token.get_token(token)
                    userName = result.userName
                    device = DeviceToken(user_name=userName,device_token=devicetoken,device_ip=getIP(request),last_time=getCurrentTime())
                    device.save()
                except (Exception) as e:
                    resultDic.status = 1
                    resultDic.code = 14003
                    resultDic.message = '服务器内部错误'
            
    else :
        resultDic.status = 1
        resultDic.code = 14001
        resultDic.message = '请求方式不正确'

    return resultDic.archiveJson()

