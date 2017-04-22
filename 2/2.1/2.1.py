# -*- coding: utf-8 -*-

import os;
import os.path;

filePaths = []
for root, dirs, files in os.walk(
    "D:\\PDM\\2.1\\SogouC.mini\\Sample"
):
    for name in files:
        filePaths.append(os.path.join(root, name));


import codecs;

filePaths = [];
fileContents = [];
for root, dirs, files in os.walk(
    "D:\\PDM\\2.1\\SogouC.mini\\Sample"
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

#作业，把文件的分类，作为语料库数据框的新的一列，加入到语料库中。