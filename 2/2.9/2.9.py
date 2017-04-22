# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:43:42 2016

@author: fangx
"""
import os;
import numpy;
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
    segments = []
    filePath = row['filePath']
    fileContent = row['fileContent']
    segs = jieba.cut(fileContent)    
    for seg in segs:
        if zhPattern.search(seg):
            segments.append(seg)
    filePaths.append(filePath)
    row['fileContent'] = " ".join(segments);

from sklearn.feature_extraction.text import CountVectorizer

stopwords = pandas.read_csv(
    "StopwordsCN.txt", 
    encoding='utf8', 
    index_col=False,
    quoting=3,
    sep="\t"
)

countVectorizer = CountVectorizer(
    stop_words=list(stopwords['stopword'].values),
    min_df=0, token_pattern=r"\b\w+\b"
)
textVector = countVectorizer.fit_transform(corpos['fileContent'])

from sklearn.metrics import pairwise_distances

distance_matrix = pairwise_distances(
    textVector, 
    metric="cosine"
)

m = 1- pandas.DataFrame(distance_matrix)
m.columns = filePaths;
m.index = filePaths;

sort = numpy.argsort(distance_matrix, axis=1)[:, 1:6]

similarity5 = pandas.Index(filePaths)[sort].values

similarityDF = pandas.DataFrame({
    'filePath':corpos.filePath, 
    's1': similarity5[:, 0], 
    's2': similarity5[:, 1], 
    's3': similarity5[:, 2], 
    's4': similarity5[:, 3], 
    's5': similarity5[:, 4]
})
