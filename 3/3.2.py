# -*- coding: utf-8 -*-
import time;
import urllib.request;
from pandas import DataFrame;
from bs4 import BeautifulSoup;
from urllib.error import URLError;

def readList(url):
    do = True
    sleepSecond = 1
    hrefs = [];
    titles = [];
    pdates = [];

    while do:
        time.sleep(sleepSecond)
        try:
            response = urllib.request.urlopen(url);
            html = response.read();
            html = html.decode('utf-8')
            soup = BeautifulSoup(html);
            ul = soup.find(attrs={"class":"gllist"})
            lis = ul.findAll('li')

            for li in lis:
                href = li.find('a').attrs['href']
                title = li.find('a').text
                pdate = li.find('span').text
                hrefs.append(href);
                titles.append(title);
                pdates.append(pdate);
        except URLError as e:
            print(e);
        else:
            do = False;
    return (hrefs, titles, pdates)

hrefs, titles, pdates = readList(
    'http://www.gd.gov.cn/govpub/xxts/index.htm'
)

response = urllib.request.urlopen(
    'http://www.gd.gov.cn/govpub/xxts/index.htm'
);
html = response.read().decode('utf-8');
pageTag = "var countPage = ";
pageStart = html.find(pageTag) + len(pageTag);
pageEnd = pageStart + 2;
pages = int(html[pageStart: pageEnd]);

for page in range(1, pages):
    url = 'http://www.gd.gov.cn/govpub/xxts/index_%d.htm' % (page)
    print(url)
    _hrefs, _titles, _pdates = readList(url)
    hrefs.extend(_hrefs)
    titles.extend(_titles)
    pdates.extend(_pdates)

def readPage(url):
    print(url);
    do = True
    sleepSecond = 1
    content = "";

    while do:
        time.sleep(sleepSecond)
        try:
            response = urllib.request.urlopen(url);
            html = response.read();
            html = html.decode('utf-8')
            soup = BeautifulSoup(html);
            contentDiv = soup.find("div", {'class': 'content'});

            if contentDiv == None:
                content = soup.text;
            else:
                content = contentDiv.text
        except URLError as e:
            print(e);
        else:
            do = False;
    content = content.strip().replace("\n", '')
    return content;

contents = []
for href in hrefs:
    content = readPage(href);
    contents.append(content);

result = DataFrame({
    'href': hrefs,
    'title': titles,
    'pdate': pdates,
    'content': contents
})

result.to_csv(
    "C:\\微云同步盘\\课程定版\\中山大学Python数据抓取讲座\\CODE\\3\\result.csv"
)
