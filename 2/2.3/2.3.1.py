# -*- coding: utf-8 -*-
import os;
import os.path;
import codecs;

filePaths = [];
fileContents = [];
for root, dirs, files in os.walk(
    "D:\\PDM\\2.3\\SogouC.mini\\Sample"
):
    for name in files:
        filePath = os.path.join(root, name);
        filePaths.append(filePath);
        f = codecs.open(filePath, 'r', 'utf-8')
        fileContent = f.read()
        f.close()
        fileContents.append(fileContent)

import pandas;
corpos = pandas.DataFrame({
    'filePath': filePaths, 
    'fileContent': fileContents
});

import jieba

segments = []
filePaths = []
for index, row in corpos.iterrows():
    filePath = row['filePath']
    fileContent = row['fileContent']
    segs = jieba.cut(fileContent)
    for seg in segs:
        segments.append(seg)
        filePaths.append(filePath)

segmentDataFrame = pandas.DataFrame({
    'segment': segments, 
    'filePath': filePaths
});


import numpy;
#进行词频统计        
segStat = segmentDataFrame.groupby(
            by="segment"
        )["segment"].agg({
            "计数": numpy.size
        }).reset_index().sort(
            columns=["计数"],
            ascending=False
        );

#移除停用词
stopwords = pandas.read_csv(
    "D:\\PDM\\2.3\\StopwordsCN.txt", 
    encoding='utf8', 
    index_col=False
)

fSegStat = segStat[
    ~segStat.segment.isin(stopwords.stopword)
]

