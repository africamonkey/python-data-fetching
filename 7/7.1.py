# -*- coding: utf-8 -*-

import json
import time
import urllib.request
import pandas
from bs4 import BeautifulSoup
from urllib.error import URLError

def readList(url):
    do = True
    sleepSecond = 1
    
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    
    ips = [];
    ports = [];

    while do:
        time.sleep(sleepSecond)
        try:
            request = urllib.request.Request(url, headers = headers)
            response = urllib.request.urlopen(request);
            html = response.read();
            html = html.decode('utf-8')
            soup = BeautifulSoup(html);
            ul = soup.find(attrs={"id":"ip_list"})
            trs = ul.findAll('tr', attrs={"class":"odd"})
            trs2 = ul.findAll('tr', attrs={"class":""})
            trs.extend(trs2)
            for tr in trs:
                tds = tr.findAll('td')
                now = 0
                for td in tds:
                    if (now == 1):
                        ip = td.getText()
                    if (now == 2):
                        port = td.getText()
                    now = now + 1
                
                print ("ip = %s, port = %s" % (ip, port))
                proxy = '%s:%s' % (ip, port)
                
                request = urllib.request.Request("http://m.weibo.cn/api/statuses/repostTimeline?id=4086433809517314&page=20", headers = headers)
                request.set_proxy(proxy, 'http')
                ok = 0
                cnt = 5
                for i in range(1, cnt):
                    ok = ok + 1
                    if (ok < i):
                        break
                    try:
                        urllib.request.urlopen(request, timeout = 1)
                        jsonBytes = response.read()
                        jsonString = jsonBytes.decode('utf8')
                        json.loads(jsonString)
                    except:
                        ok = ok - 1
                if (ok >= cnt - 1):
                    print ("check success %d ==========================================================" % (ok))
                    ips.append(ip);
                    ports.append(port);
                else:
                    print ("check fail %d" % (ok))
        except URLError as e:
            print(e);
        else:
            do = False;
    return (ips, ports)

page_start = 1
page_end = 50
ips = []
ports = []

for page in range(page_start, page_end):
    url = 'http://www.xicidaili.com/wt/%d' % (page)
    print(url)
    _ips, _ports = readList(url)
    ips.extend(_ips)
    ports.extend(_ports)
    if (page % 10 == 0):
        proxies = pandas.DataFrame({'ip':ips, 'port':ports})
        proxies.to_csv("temp/proxy_%d.csv" % (page / 10), index=False)
    
proxies = pandas.DataFrame({'ip':ips, 'port':ports})
proxies.to_csv("proxy.csv", index=False)
