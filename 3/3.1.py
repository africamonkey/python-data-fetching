# -*- coding: utf-8 -*-
import urllib.request;
from bs4 import BeautifulSoup;

response = urllib.request.urlopen(
    'http://www.gd.gov.cn/govpub/xxts/index.htm'
);

html = response.read();

html = html.decode('utf-8')

soup = BeautifulSoup(html);

ul = soup.find(attrs={"class":"gllist"})

lis = ul.findAll('li')

for li in lis:
    print(li.find('a').attrs['href'])
    print(li.find('a').text)
    print(li.find('span').text)
