# -*- coding: utf-8 -*-
import os
import codecs
import pandas
import jieba
import jieba.analyse

filePaths = []
contents = []
tag1s = []
tag2s = []
tag3s = []
tag4s = []
tag5s = []

for root, dirs, files in os.walk(
    "D:\\PDM\\2.6\\SogouC.mini\\Sample\\"
):
    for name in files:
        filePath = root + '\\' + name;
        f = codecs.open(filePath, 'r', 'utf-8')
        content = f.read().strip()
        f.close()
        tags = jieba.analyse.extract_tags(content, topK=5)
        filePaths.append(filePath)
        contents.append(content)
        tag1s.append(tags[0])
        tag2s.append(tags[1])
        tag3s.append(tags[2])
        tag4s.append(tags[3])
        tag5s.append(tags[4])

tagDF = pandas.DataFrame({
    'filePath': filePaths, 
    'content': contents, 
    'tag1': tag1s, 
    'tag2': tag2s, 
    'tag3': tag3s, 
    'tag4': tag4s, 
    'tag5': tag5s
})
