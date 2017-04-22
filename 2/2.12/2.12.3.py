# -*- coding: utf-8 -*-

import os
import codecs
import os.path

classDict = {
    'C000008': '财经',
    'C000010': 'IT',
    'C000013': '健康',
    'C000014': '体育',
    'C000016': '旅游',
    'C000020': '教育',
    'C000022': '招聘',
    'C000023': '文化',
    'C000024': '军事'
}

rootDir = "D:\\PDM\\2.12\\Reduced"

classes = [];
filePaths = [];
fileContents = [];
for c in classDict.keys():
    fileDir = os.path.join(rootDir, c)
    for root, dirs, files in os.walk(fileDir):
        for name in files:
            filePath = os.path.join(fileDir, name);
            
            try:
                f = codecs.open(filePath, 'r', 'gb2312')
                fileContent = f.read()
                f.close()
                fileContents.append(fileContent)
                classes.append(classDict[c]);
                filePaths.append(filePath);
            except Exception as e:
                print(filePath)
                
import pandas;
corpos = pandas.DataFrame({
    'class': classes,
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
    "D:\\PDM\\2.12\\StopwordsCN.txt", 
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

#正交分析法
from sklearn.decomposition import TruncatedSVD

n_topics = 9
truncatedSVD = TruncatedSVD(
    n_components=n_topics
).fit(textVector)
topicWordMatrix = truncatedSVD.components_

import numpy;
prefixMatrix = numpy.where(topicWordMatrix>=0, "", "^")

sort = numpy.argsort(
    -1*numpy.abs(topicWordMatrix), 
    axis=1
)[:, 0:20]

prefixs = []
for i in range(9):
    prefixs.append(prefixMatrix[i, sort[i]])

keywords = pandas.Index(countVectorizer.get_feature_names())[sort].values

print(prefixs+ keywords)
textTopicMatrix = truncatedSVD.fit_transform(textVector)

corpos['topic'] = textTopicMatrix.argmax(axis=1)

pandas.crosstab(corpos['class'], corpos['topic'])

