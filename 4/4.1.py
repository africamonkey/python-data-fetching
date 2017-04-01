# -*- coding: utf-8 -*-
import json;
import urllib.parse
import urllib.request

page = 1
weiboId = 4089311604948232

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

dataURL = 'http://m.weibo.cn/api/statuses/repostTimeline?id=%d&page=%d' % (weiboId, page);
req = urllib.request.Request(
    dataURL,
    headers=headers,
    proxies=proxies,
    timeout=1
)
response = urllib.request.urlopen(req)
jsonString = response.read()
jsonObject = json.loads(jsonString.decode('utf8'))
for data in jsonObject['data']:
    print(data['raw_text'])




for page in range(1, 2069):
    dataURL = 'http://m.weibo.cn/api/statuses/repostTimeline?id=%d&page=%d' % (weiboId, page);
    req = urllib.request.Request(dataURL, headers=headers)
    response = urllib.request.urlopen(req)
    jsonString = response.read()
    jsonObject = json.loads(jsonString.decode('utf8'))
    for data in jsonObject['data']:
        print(data['raw_text'])
