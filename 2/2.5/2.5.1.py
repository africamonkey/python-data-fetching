# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 22:49:20 2016

@author: fangx
"""

import jieba
import numpy
import codecs
import pandas

file = codecs.open("D:\\PDM\\2.5\\红楼梦.txt", 'r', 'utf-8')
content = file.read()
file.close()

jieba.load_userdict('D:\\PDM\\2.5\\红楼梦词库.txt');

segments = []
segs = jieba.cut(content)
for seg in segs:
    if len(seg)>1:
        segments.append(seg);
    
segmentDF = pandas.DataFrame({'segment':segments})

#移除停用词
stopwords = pandas.read_csv(
    "D:\\PDM\\2.5\\StopwordsCN.txt", 
    encoding='utf8', 
    index_col=False,
    quoting=3,
    sep="\t"
)

segmentDF = segmentDF[~segmentDF.segment.isin(stopwords.stopword)]

wyStopWords = pandas.Series([
  # 42 个文言虚词 
  '之', '其', '或', '亦', '方', '于', '即', '皆', '因', '仍', '故', 
  '尚', '呢', '了', '的', '着', '一', '不', '乃', '呀', '吗', '咧', 
  '啊', '把', '让', '向', '往', '是', '在', '越', '再', '更', '比', 
  '很', '偏', '别', '好', '可', '便', '就', '但', '儿', 
  # 高频副词 
  '又', '也', '都', '要', 
  # 高频代词 
  '这', '那', '你', '我', '他',
  #高频动词
  '来', '去', '道', '笑', '说',
  #空格
  ' ', ''
]);

segmentDF = segmentDF[~segmentDF.segment.isin(wyStopWords)]

segStat = segmentDF.groupby(
            by=["segment"]
        )["segment"].agg({
            "计数":numpy.size
        }).reset_index().sort(
            columns=["计数"],
            ascending=False
        );
    
segStat.head(100)


#绘画词云
#http://www.lfd.uci.edu/~gohlke/pythonlibs/
from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud = WordCloud(
    font_path='D:\\simhei.ttf', 
    background_color="black"
)

words = segStat.set_index('segment').to_dict()

wordcloud = wordcloud.fit_words(words['计数'])

#适配老版本的语句
#wordcloud = wordcloud.fit_words(fSegStat.itertuples(index=False))

plt.imshow(wordcloud)

plt.close()
