#!/user/bin/python3
#coding:utf-8

from http.client import HTTPConnection
import json
import zlib

def run(url,params,token):
    httpClient = None
    data=None
    try:
        httpClient = HTTPConnection('192.168.106.92', 8880)
        if token=='':
            headers = {'content-type': 'application/json', 'Accept-Language': 'zh-CN'}  # post请求头需要有content-type
        else:
            headers = {'content-type': 'application/json;', 'Accept-Language': 'zh-CN','token':'%s'%(token)}  # 加入token



        json_str = json.dumps(params)

        httpClient.request('POST', url, json_str, headers)  # 这里可以不带key，直接用value
        response = httpClient.getresponse()
        #print(response.getheaders())
        data=json.loads(response.read().decode(encoding='utf-8'))# 将获取到的内容转换为json类型数据
       # data = json.loads(response, encoding='utf-8')
        #f=json.loads(response.read())# 将获取到的内容转换为json类型数据
       # print(f['code'])
        #data = response.getcode()

    except Exception:
        print("error")
    finally:
        if httpClient:
            httpClient.close()
        return data

def run_post2(url,params,token):
    httpClient = None
    data=None

    try:
        httpClient = HTTPConnection('192.168.117.58', 8003)
        if token == '':
            headers = {'Accept': 'application/json;charset=UTF-8',
                       'Content-Type': 'application/x-www-form-urlencoded'}  # post请求头需要有content-type
        else:
            headers = {'Accept': 'application/json;charset=UTF-8', 'Content-Type': 'application/x-www-form-urlencoded',
                       'token': '%s' % (token)}  # 加入 token
        # json_str = json.dumps(params)
        httpClient.request('POST', url, params, headers)  # 这里可以不带key，直接用value
        response = httpClient.getresponse()
        data = json.loads(response.read().decode(encoding='utf-8'))  # 将获取到的内容转换为json类型数据
    except Exception:
        print("error")
    finally:
        if httpClient:
            httpClient.close()
        return data
