# -*- coding: utf-8 -*-

import jieba
import pandas
import jieba.analyse
from sklearn.feature_extraction.text import CountVectorizer

data = pandas.read_excel("D:\\PDM\\2.11\\comments.xlsx")

stopwords = pandas.read_csv(
    "D:\\PDM\\2.11\\StopwordsCN.txt", 
    encoding='utf8', 
    index_col=False,
    quoting=3,
    sep="\t"
)

jieba.load_userdict('D:\\PDM\\2.11\\words.txt');

words = []
for content in data['comments']:
    segs = jieba.cut(content)
    words.append(" ".join(segs))

countVectorizer = CountVectorizer(
    stop_words=list(stopwords['stopword'].values),
    min_df=0, token_pattern=r"\b\w+\b"
)
textVector = countVectorizer.fit_transform(words)


from sklearn.naive_bayes import MultinomialNB
MNBModel = MultinomialNB()

MNBModel.fit(textVector, data.ratings)

MNBModel.score(textVector, data.ratings)

uComment = [
    "这部电影，没啥意思，剧情老套，真没劲, 后悔来看了。",
    "太精彩了，讲了一个关于梦想的故事剧情很反转制作也很精良"
]

uWords = []
for content in uComment:
    segs = jieba.cut(content)
    uWords.append(" ".join(segs))

uTextVector = countVectorizer.transform(uWords)

MNBModel.predict(uTextVector)