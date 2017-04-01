#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
Created on 2017年3月31日

@author: LFly
'''
import json
import urllib.parse
import urllib.request
import os



#网站源：全国中小企业股份转让系统
contextPath = "http://www.neeq.com.cn"
   
#通过此post请求获取数据
url="http://www.neeq.com.cn/disclosureInfoController/infoResult.do"

#在E盘符下建立文件夹
if os.path.exists('E:\\pdf_download'):
    print("Folder already exists")
else:
    os.mkdir('E:\\pdf_download')
    
#切换到该目录下
os.chdir('E:\\pdf_download')

def downloadPDF(url):
    print('download starting ---- from %s  '%(url))
    
    
    #拼接文件名
    filename = url[url.find('disclosure/')+11:].replace('/','_')

    response = urllib.request.urlopen(url)
    print("filename -- %s"%(filename))
    fp = open(filename,'wb')
    
    block_sz = 8192
    while True:
        buffer = response.read(block_sz)
        if not buffer:
            break
        
        fp.write(buffer)
    
    fp.close()
    print('dowload succefully \n')


def postHttp(disclosureType=None,page=None,companyCd=None,
       isNewThree=None,startTime=None,endTime=None,
       keyword=None,xxfcbj=None):

    #提交的参数
    postdata=dict(disclosureType=disclosureType,page=page,companyCd=companyCd,isNewThree=isNewThree,
         startTime=startTime,endTime=endTime,keyword=keyword,xxfcbj=xxfcbj)
  
    #url编码  post请求参数
    postdata=urllib.parse.urlencode(postdata).encode(encoding='utf_8')
    
    request = urllib.request.Request(url,postdata)
    request.add_header('Content-Type',"application/x-www-form-urlencoded");
    request.add_header('Accept',"text/plain");
    
    #返回json数据
    response = urllib.request.urlopen(request)
    
    #根据返回的数据作出相应的处理     截取json字符串
    rawData = response.read().decode("utf_8")
    
    #根据返回数据格式做相应操作
    if(rawData[0:4]=="null"):
        jsonArray = rawData[5:-1]
    else:
        jsonArray = rawData[:-1]
    
    #打印截取后的json字符串
    print("json data from server --- \n %s"%(jsonArray))
    
    
    json2dit = json.loads(jsonArray)
    contents = json2dit[0]['listInfo']['content']
    
    print("\n")
    for companyInfo in contents:
        downloadPDF(contextPath+companyInfo['destFilePath'])
    
#对应的参数  需要自己设置
postHttp("5","1","","1","2016-02-01","2017-03-31","","1")


    