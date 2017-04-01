# -*- coding: utf-8 -*-
import jieba
import numpy
import codecs
import pandas

file = codecs.open(
    "D:\\PNC\\4\\content.csv", 'r', 'utf-8'
)
content = file.read()
file.close()

segments = []
segs = jieba.cut(content)
for seg in segs:
    if len(seg)>1:
        segments.append(seg)

segmentDF = pandas.DataFrame({'segment':segments})

#移除停用词
stopwords = pandas.read_csv(
    "D:\\pnc\\4.1\\StopwordsCN2.txt",
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

segStat = segmentDF.groupby(
            by=["segment"]
        )["segment"].agg({
            "计数":numpy.size
        }).reset_index().sort(
            columns=["计数"],
            ascending=False
        )

segStat.head(100)

#绘画词云
#http://www.lfd.uci.edu/~gohlke/pythonlibs/
from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud = WordCloud(
    font_path='D:\\PNC\\4.1\\simhei.ttf',
    background_color="black"
)

words = segStat.set_index('segment').to_dict()

wordcloud = wordcloud.fit_words(words['计数'])

plt.figure(
    num=None, figsize=(30, 20),
    dpi=500, facecolor='w', edgecolor='k'
)

plt.axis("off")
plt.imshow(wordcloud)
plt.show()


plt.close()
