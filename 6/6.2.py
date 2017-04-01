# -*- coding: utf-8 -*-
import os
import urllib
import pandas

keyword = '刺死辱母者被判无期'
data = pandas.read_csv(
    "D:\\PNC\\6\\weibo_search_%s.csv" % (keyword)
)

directory = "D:\\PNC\\6\\%s" % (keyword);
if not os.path.exists(directory):
    os.makedirs(directory)

data = data.dropna()

import urllib.request
opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')

for index, row in data.iterrows():
    wId = row['id']
    imageURL = row['pics']
    localFile = "%s\\%s.png" % (directory, wId);
    try:
        filename, headers = opener.retrieve(imageURL, localFile);
    except Exception as e:
        print(str(e))
