# -*- coding: utf-8 -*-
import time
import json
import numpy
import pandas
import urllib.parse
import urllib.request

commentAPI = 'http://m.weibo.cn/api/statuses/repostTimeline?id=%d&page=%d'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

def getJSONObject(weiboId, page):
    do = True
    sleepSecond = 1
    jsonObject = ""

    while do:
        time.sleep(sleepSecond)
        dataURL = commentAPI % (weiboId, page)
        print("处理 URL: %s" % (dataURL))

        req = urllib.request.Request(dataURL, headers=headers)

        response = urllib.request.urlopen(req)
        jsonBytes = response.read()
        jsonString = jsonBytes.decode('utf8')
        jsonObject = json.loads(jsonString)

        if 'data' not in jsonObject:
            sleepSecond = sleepSecond+5
            print("遭受限制~~~，%s 秒后重试" % (sleepSecond))
            continue
        else :
            do = False

    return jsonObject

testObject = getJSONObject(4086433809517314, 20)

weiboIds = pandas.read_csv(
    "D:\\PNC\\4\\weiboIds.csv"
).weiboId

"""
    处理要处理的数据 start
"""
pids = []
pages = []

for pid in weiboIds:
    page = 1
    jsonObject = getJSONObject(pid, page)
    totalPage = jsonObject['max']
    for page in range(1, totalPage+1):
        pages.append(page)
        pids.append(pid)

allNeed = pandas.DataFrame({'pid':pids, 'page':pages})

allNeed.to_csv("D:\\PNC\\4\\allNeed.csv", index=False)

"""
    处理要处理的数据 end
"""


allNeed = pandas.read_csv(
    "D:\\PNC\\4\\allNeed.csv",
    dtype=(numpy.int64, numpy.int64)
)
completed = pandas.read_csv(
    "D:\\PNC\\4\\completed.csv",
    dtype=(numpy.int64, numpy.int64)
)
needToGet = allNeed[
    pandas.DataFrame.all(
        ~allNeed.isin(completed),
        axis=1
    )
]


while needToGet.size>0:
    completedPIDs = []
    completedPages = []
    for index, row in needToGet.iterrows():
        pid = row['pid']
        page = row['page']

        try:
            contents = []
            comments = jsonObject['data']
            jsonObject = getJSONObject(pid, page)

            for comment in comments:
                contents.append(comment['raw_text'])

            contentDF = pandas.DataFrame({'contents': contents})
            contentDF.to_csv(
                'D:\\PNC\\4\\content.csv',
                mode='a', header=False, index=False
            )
            completedPIDs.append(pid)
            completedPages.append(page)
        except Exception as e:
            print(str(e))

    newCompleted = pandas.DataFrame({
            'pids':completedPIDs,
            'pages':completedPages
        },
        dtype=(numpy.int64, numpy.int64)
    )
    newCompleted.to_csv(
        "D:\\PNC\\4\\completed.csv",
        mode='a', header=False, index=False
    )
    completed = pandas.read_csv(
        "D:\\PNC\\4\\completed.csv",
        dtype=(numpy.int64, numpy.int64)
    )
    needToGet = allNeed[
        pandas.DataFrame.all(
            ~allNeed.isin(completed), axis=1
        )
    ]
