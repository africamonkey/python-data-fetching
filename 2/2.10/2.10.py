# -*- coding: utf-8 -*-
import re
import os
import jieba
import codecs
import numpy
import pandas
import os.path
from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction.text import CountVectorizer

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

corpos = pandas.DataFrame({
    'filePath': filePaths, 
    'fileContent': fileContents
});

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

contents = []
summarys = []
filePaths = []

for index, row in corpos.iterrows():
    filePath = row['filePath']
    fileContent = row['fileContent']
    #建立子语料库，以该文档和该文档的分句组成
    subCorpos = [fileContent] + re.split(
        r'[。？！\n]\s*', 
        fileContent
    )
    
    segments = []
    suitCorpos = []
    for content in subCorpos:
        segs = jieba.cut(content)
        segment = " ".join(segs)
        if len(segment.strip())>10:
            segments.append(segment)
            suitCorpos.append(content)

    textVector = countVectorizer.fit_transform(segments)

    distance_matrix = pairwise_distances(
        textVector, 
        metric="cosine"
    )
    
    sort = numpy.argsort(distance_matrix, axis=1)
    
    summary = pandas.Index(suitCorpos)[sort].values[0]
    
    summarys.append(summary)    
    filePaths.append(filePath)
    contents.append(fileContent)

summaryDF = pandas.DataFrame({
    'filePath': filePaths,
    'content': contents,
    'summary': summarys
})
