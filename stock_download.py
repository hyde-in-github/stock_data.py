# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import urllib2
from BeautifulSoup import BeautifulSoup
import re

# <codecell>

#找到数列中非空
def fnn(List):
    for item in List:
        if item != '':
            return item

# <codecell>

class stockdata:
    def __init__(self):
        self.stock = {}
    def init(self):
        pattern1 = re.compile(r'"stockid.*?"}')
        pattern2 = re.compile(r'","')
        pattern3 = re.compile(r'"stockcode":"\d+"')
        pattern4 = re.compile(r'\d+')
        total = ""
        for i in range(52):
            html = urllib2.urlopen('http://q.10jqka.com.cn/interface/stock/fl/zdf/desc/'+str(i+1)+'/hsa/quote')
            total += str(BeautifulSoup(html))
        stock_pri = pattern1.findall(total)
        for s in stock_pri:
            stockcode = pattern4.findall(pattern3.findall(s)[0])[0]
            self.stock[stockcode] = {}
            stock_0 = s.split(',')
            for Ele in stock_0[:-1]:
                if Ele == '"stockname":null':
                    continue
                bre = Ele.split('":"')
                self.stock[stockcode][fnn(bre[0].split('"'))] = fnn(bre[1].split('"'))

# <codecell>

s = stockdata()

# <codecell>

s.init()

# <codecell>

f = open('/home/hyde/Documents/stock.txt', 'w')
for i in s.stock:
    for j in s.stock[i]:
        if j != u'stockname':
            f.write(str(s.stock[i][j]))
            f.write(',')
    f.write('\n')

# <codecell>

