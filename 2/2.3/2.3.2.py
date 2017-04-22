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
import numpy

segments = []
filePaths = []
for index, row in corpos.iterrows():
    filePath = row['filePath']
    fileContent = row['fileContent']
    segs = jieba.cut(fileContent)
    for seg in segs:
        if seg not in stopwords.stopword.values and len(seg.strip())>0:
            segments.append(seg)
            filePaths.append(filePath)

segmentDataFrame = pandas.DataFrame({
    'segment': segments, 
    'filePath': filePaths
});

segStat = segmentDataFrame.groupby(
            by="segment"
        )["segment"].agg({
            "计数":numpy.size
        }).reset_index().sort(
            columns=["计数"],
            ascending=False
        );
