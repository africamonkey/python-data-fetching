# -*- coding: utf-8 -*-

import jieba;

for w in jieba.cut("我爱Python"):
    print(w)

for w in jieba.cut("工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作"):
    print(w)
#http://pinyin.sogou.com/dict/

seg_list = jieba.cut("真武七截阵和天罡北斗阵哪个更厉害呢？")
for w in seg_list:
    print(w)

jieba.add_word('真武七截阵')
jieba.add_word('天罡北斗阵')
seg_list = jieba.cut("真武七截阵和天罡北斗阵哪个更厉害呢？")
for w in seg_list:
    print(w)

jieba.load_userdict('D:\\PDM\\2.2\\金庸武功招式.txt');

import os;
import os.path;
import codecs;

filePaths = [];
fileContents = [];
for root, dirs, files in os.walk(
    "D:\\PDM\\2.2\\SogouC.mini\\Sample"
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

import jieba

segments = []
filePaths = []
for index, row in corpos.iterrows():
    filePath = row['filePath']
    fileContent = row['fileContent']
    segs = jieba.cut(fileContent)
    for seg in segs:
        segments.append(seg)
        filePaths.append(filePath)

segmentDataFrame = pandas.DataFrame({
    'segment': segments, 
    'filePath': filePaths
});
