# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 21:53:37 2016

@author: TBKKEN
"""
import numpy

#创建语料库
import os;
import os.path;
import codecs;

filePaths = [];
fileContents = [];
for root, dirs, files in os.walk(
    "SogouC.mini/Sample"
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

import re
#匹配中文的分词
zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

import jieba

segments = []
filePaths = []
for index, row in corpos.iterrows():
    filePath = row['filePath']
    fileContent = row['fileContent']
    segs = jieba.cut(fileContent)
    for seg in segs:
        if zhPattern.search(seg):
            segments.append(seg)
            filePaths.append(filePath)

segmentDF = pandas.DataFrame({
    'filePath':filePaths, 
    'segment':segments
})

#移除停用词
stopwords = pandas.read_csv(
    "StopwordsCN.txt", 
    encoding='utf8', 
    index_col=False,
    quoting=3,
    sep="\t"
)

segmentDF = segmentDF[
    ~segmentDF.segment.isin(
        stopwords.stopword
    )
]

#按文章进行词频统计
segStat = segmentDF.groupby(
    by=["filePath", "segment"]
)["segment"].agg({
    "计数":numpy.size
}).reset_index().sort(
    columns=["计数"],
    ascending=False
);

#把小部分的数据删除掉
segStat = segStat[segStat.计数>1]

#进行文本向量计算
TF = segStat.pivot_table(
    index='filePath', 
    columns='segment', 
    values='计数',
    fill_value=0
)

TF.index
TF.columns

def hanlder(x): 
    return (numpy.log2(len(corpos)/(numpy.sum(x>0)+1)))

IDF = TF.apply(hanlder)

TF_IDF = pandas.DataFrame(TF*IDF)

tag1s = []
tag2s = []
tag3s = []
tag4s = []
tag5s = []

for filePath in TF_IDF.index:
    tagis = TF_IDF.loc[filePath].order(
        ascending=False
    )[:5].index
    tag1s.append(tagis[0])
    tag2s.append(tagis[1])
    tag3s.append(tagis[2])
    tag4s.append(tagis[3])
    tag5s.append(tagis[4])

tagDF = pandas.DataFrame({
    'filePath':corpos.filePath, 
    'fileContent':corpos.fileContent, 
    'tag1':tag1s, 
    'tag2':tag2s, 
    'tag3':tag3s, 
    'tag4':tag4s, 
    'tag5':tag5s
})
