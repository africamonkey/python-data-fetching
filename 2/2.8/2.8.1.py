# -*- coding: utf-8 -*-
contents = [
    '我 是 中国 人。',
    '你 是 美国 人。',
    '他 叫 什么 名字？',
    '她 是 谁 啊？'
];

from sklearn.feature_extraction.text import CountVectorizer

countVectorizer = CountVectorizer()
textVector = countVectorizer.fit_transform(contents);

textVector.todense()
countVectorizer.vocabulary_


countVectorizer = CountVectorizer(
    min_df=0, 
    token_pattern=r"\b\w+\b"
)
textVector = countVectorizer.fit_transform(contents);

textVector.todense()
countVectorizer.vocabulary_

from sklearn.feature_extraction.text import TfidfTransformer

transformer = TfidfTransformer()
tfidf = transformer.fit_transform(textVector)

import pandas;
TFIDFDataFrame = pandas.DataFrame(tfidf.toarray());
TFIDFDataFrame.columns = countVectorizer.get_feature_names();


import numpy;
TFIDFSorted = numpy.argsort(tfidf.toarray(), axis=1)[:, -2:]

TFIDFDataFrame.columns[TFIDFSorted].values
