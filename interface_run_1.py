#!/user/bin/python3
#coding:utf-8

from http.client import HTTPConnection
import json
import zlib

def run(url,params):
    httpClient = None
    data=None

    httpClient = HTTPConnection('192.168.106.92', 8880)

    headers = {'content-type': 'application/json','Accept-Language':'zh-CN'}  # post请求头需要有content-type
    json_str = json.dumps(params)

    httpClient.request('POST', url, json_str, headers)  # 这里可以不带key，直接用value



    response = httpClient.getresponse()
    print(response.getheaders())
    d=response.read().decode(encoding='utf-8')
    print(d)
    #print(zlib.decompress(data, 16+zlib.MAX_WBITS))
    data=json.loads(d, encoding='utf-8')


        #d=data.decode(encode='utf-8')

    print(data)
       # data = json.loads(response, encoding='utf-8')
        #f=json.loads(response.read())# 将获取到的内容转换为json类型数据
       # print(f['code'])
        #data = response.getcode()


    if httpClient:
        httpClient.close()
    return data
