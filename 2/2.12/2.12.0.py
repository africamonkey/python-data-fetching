# -*- coding: utf-8 -*-

import os
import codecs
import os.path

classDict = {
    'C000007': '汽车',
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

rootDir = "D:\\PDM\\2.10\\SogouC.mini\\Sample"

classes = [];
filePaths = [];
fileContents = [];
for c in classDict.keys():
    fileDir = os.path.join(rootDir, c)
    for root, dirs, files in os.walk(fileDir):
        for name in files:
            filePath = os.path.join(fileDir, name);
            classes.append(classDict[c]);
            filePaths.append(filePath);
            f = codecs.open(filePath, 'r', 'utf-8')
            fileContent = f.read()
            f.close()
            fileContents.append(fileContent)

import pandas;
corpos = pandas.DataFrame({
    'class': classes,
    'filePath': filePaths, 
    'fileContent': fileContents
});


import re
import jieba

#匹配中文的分词
zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
jieba.load_userdict('D:\\PDM\\2.12\\words.txt');

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
from sklearn.feature_extraction.text import TfidfTransformer

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

transformer = TfidfTransformer()
tfidf = transformer.fit_transform(textVector)

from sklearn.decomposition import LatentDirichletAllocation

n_topics = 10
lda = LatentDirichletAllocation(
    n_topics=n_topics
)
lda.fit(textVector)

topicWordMatrix = lda.components_

import numpy;
sort = numpy.argsort(-1*topicWordMatrix, axis=1)[:, 0:10]

keywords = pandas.Index(countVectorizer.get_feature_names())[sort].values
print(keywords)

textTopicMatrix = lda.fit_transform(textVector)

corpos['topic'] = textTopicMatrix.argmax(axis=1)


lda = LatentDirichletAllocation(
    n_topics=n_topics
)
lda.fit(tfidf)

topicWordMatrix = lda.components_

import numpy;
sort = numpy.argsort(-1*topicWordMatrix, axis=1)[:, 0:10]

keywords = pandas.Index(countVectorizer.get_feature_names())[sort].values
print(keywords)
