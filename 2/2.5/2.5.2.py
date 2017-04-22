# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 09:32:04 2016

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

from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

bimg = imread("D:\\PDM\\2.5\\贾宝玉.png")

wordcloud = WordCloud(
    background_color="white", 
    mask=bimg, font_path='D:\\PDM\\2.5\\simhei.ttf'
)

wordcloud = wordcloud.fit_words(words['计数'])

bimgColors = ImageColorGenerator(bimg)

plt.axis("off")
plt.imshow(wordcloud.recolor(color_func=bimgColors))
plt.show()



bimg = imread("D:\\PDM\\2.5\\贾宝玉2.png")

wordcloud = WordCloud(
    background_color="white", 
    mask=bimg, font_path='D:\\PDM\\2.5\\simhei.ttf'
)

wordcloud = wordcloud.fit_words(words['计数'])

plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')

bimgColors = ImageColorGenerator(bimg)

plt.axis("off")
plt.imshow(wordcloud.recolor(color_func=bimgColors))
plt.show()
