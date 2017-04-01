# -*- coding: utf-8 -*-
import time
import json
import pandas
import urllib.parse
import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

def getJSONObject(keyword, page):
    do = True
    sleepSecond = 1
    jsonObject = ""

    while do:
        time.sleep(sleepSecond)
        keyword = quote(keyword)
        dataURL = 'http://m.weibo.cn/container/getIndex?type=all&queryVal=%s&luicode=10000011&lfid=100103type%%3D1%%26q%%3D%s&title=%s&containerid=100103type%%3D1%%26q%%3D%s&page=%d' % (keyword, keyword, keyword, keyword, page)

        print("处理 URL: %s" % (dataURL))

        req = urllib.request.Request(dataURL, headers=headers)

        response = urllib.request.urlopen(req)
        jsonBytes = response.read()
        jsonString = jsonBytes.decode('utf-8')
        jsonObject = json.loads(jsonString)

        if 'cards' not in jsonObject:
            sleepSecond = sleepSecond+5
            print("遭受限制~~~，%s 秒后重试" % (sleepSecond))
            continue
        else :
            do = False

    return jsonObject

page = 0
keyword = '刺死辱母者被判无期'

do = True
weiboIds = []
weiboTexts = []
while do:
    print("page:" + str(page))
    resultObject = getJSONObject(keyword, page)
    cards = resultObject['cards']
    if len(cards)==0:
            do = False
            continue
    for card in cards:
        cardGroups = card['card_group']

        for group in cardGroups:
            if 'mblog' in group:
                html = group['mblog']['text']
                soup = BeautifulSoup(html)
                weiboId = group['mblog']['id']
                weiboIds.append(weiboId)
                weiboTexts.append(soup.text)
    page = page + 1

data = pandas.DataFrame({
    'id': weiboIds,
    'text': weiboTexts
})

data.to_csv("D:\\PNC\\5\\weibo_search_" + keyword + ".csv", encoding='utf-8', index=False)
