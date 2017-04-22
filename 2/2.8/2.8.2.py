# -*- coding: utf-8 -*-
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
from sklearn.feature_extraction.text import TfidfTransformer

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

transformer = TfidfTransformer()
tfidf = transformer.fit_transform(textVector)

import numpy;
sort = numpy.argsort(tfidf.toarray(), axis=1)[:, -5:]
names = countVectorizer.get_feature_names();

keywords = pandas.Index(names)[sort].values

tagDF = pandas.DataFrame({
    'filePath':corpos.filePath, 
    'fileContent':corpos.fileContent, 
    'tag1':keywords[:, 0], 
    'tag2':keywords[:, 1], 
    'tag3':keywords[:, 2], 
    'tag4':keywords[:, 3], 
    'tag5':keywords[:, 4]
})
