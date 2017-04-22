# -*- coding: utf-8 -*-

import time
import pandas
import requests
from bs4 import BeautifulSoup;
from requests.exceptions import Timeout;

url = "https://movie.douban.com/subject/26260853/comments?start=%d&limit=%d&sort=new_score&status=P"

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cookie':'bid=vbOxLrNxLek; ll="118281"; __utma=30149280.1080239476.1480080075.1480080075.1480080075.1; __utmz=30149280.1480080075.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; gr_user_id=4af3549d-c1ac-43b7-aa80-cdf210408ca0; viewed="5257905_25779298_4816562_10020265"; _vwo_uuid_v2=5389494DD2833D64A584F83CD4C12CE2|0d1043bd74fb33394316959a88e70fdf; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1492574574%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; ps=y; ue="fangxiaomin11@163.com"; dbcl2="135170273:JVMHELP1Vec"; ck=oElB; ap=1; _pk_id.100001.4cf6=764c3ed2264fb389.1477538782.3.1492576065.1492571784.; _pk_ses.100001.4cf6=*; push_noty_num=0; push_doumail_num=0',
    'Host':'movie.douban.com',
    'Referer':'https://movie.douban.com/subject/26260853/comments?start=20&limit=20&sort=new_score&status=P',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

def getContent(page):
    do = True;
    sleepSecond = 0
    _voteses = []
    _seens = []
    _comments = []
    _ratings = []
    _pTimes = []
    while do:
        time.sleep(sleepSecond)
        try:
            result = requests.get(
                url % (20*(page-1), 20), headers=headers, timeout=2
            )
            rString = result.content.decode('UTF-8')
            
            soup = BeautifulSoup(rString)
            commentDivs = soup.findAll(attrs={
                'class': "comment"
            })
            for commentDiv in commentDivs:
                votes = commentDiv.find(
                    "span", attrs={
                        'class': "votes"
                    }
                ).text
                commentInfoSpan = commentDiv.find(
                    "span", attrs={
                        'class': "comment-info"
                    }
                )
                spans = commentInfoSpan.findAll(
                    "span"
                )
                seen, rating, pTime = "", "", ""
                if len(spans)==3:
                    seen, rating, pTime = spans;
                    seen = seen.text
                    rating = rating.attrs['title']
                    pTime = pTime.attrs['title']
                elif len(spans)==2:
                    seen, pTime = spans;
                    seen = seen.text
                    rating = "暂无"
                    pTime = pTime.attrs['title']
                    
                comment = commentDiv.find(
                    "p", attrs={
                        'class': ""
                    }
                ).text
                _voteses.append(votes)
                _seens.append(seen)
                _ratings.append(rating)
                _pTimes.append(pTime)
                _comments.append(comment)
        except Timeout as te:
            print(te)
            print("连接超时了。")
            sleepSecond = sleepSecond + 1
        except Exception as e:
            print(e);
            sleepSecond = sleepSecond + 1
        else:
            do = False;
    return _voteses, _seens, _ratings, _pTimes, _comments;

page = 1;
do = True
voteses, seens, ratings, pTimes, comments = [], [], [], [], []
while do:
    _voteses, _seens, _ratings, _pTimes, _comments = getContent(page)
    voteses.extend(_voteses)
    seens.extend(_seens)
    ratings.extend(_ratings)
    pTimes.extend(_pTimes)
    comments.extend(_comments)
    print("完成抓取: " + str(page))
    print("现在有数据: " + str(len(voteses)))
    if len(_voteses)>0:
        page = page + 1
    else:
        do = False

result = pandas.DataFrame({
    'voteses': voteses, 
    'seens': seens, 
    'ratings': ratings, 
    'pTimes': pTimes, 
    'comments': comments
})

result.to_excel("D:\\PDM\\2.12\\comments.xlsx")