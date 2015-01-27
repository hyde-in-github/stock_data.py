# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import urllib2
from BeautifulSoup import BeautifulSoup
import re
import time
import datetime
import MySQLdb
import os

# <codecell>

class stockdata:
    
    def __init__(self,path):
        self.path = path
        self.stock = {}
        try:
            os.mknod(path+'/original_time.txt')
            os.mknod(path+'/log.txt')
        except: None
    
    def num(self):
        No = 1
        fp = open(self.path + '/original_time.txt')
        time_o = float(fp.read())
        fp.close()
        
        time_n = float(time.time())
        days =  int((time_n - time_o) / (24*60*60)) 
        days_eff = (days / 7) * 5 + (days % 7)
        No += days_eff * 48

        if days == 0:
            minutes = int((time_n - time_o) / 60)
        else:
            minutes = int(((time_n - time_o) % (days_eff * 24*60*60)) / 60)
        if minutes < 11*60 + 30:
            No += (minutes / 5)
        else: 
            No += 24 + ((minutes - 13*60) / 5)
        return No
    
    def fnn(self,List):
        for item in List:
            if item != '':
                return item
            
    def surf(self):
        pattern1 = re.compile(r'"stockid.*?"}')
        pattern2 = re.compile(r'","')
        pattern3 = re.compile(r'"stockcode":"\d+"')
        pattern4 = re.compile(r'\d+')
        total = ""
        for i in range(52):
            html = urllib2.urlopen('http://q.10jqka.com.cn/interface/stock/fl/zdf/desc/'+str(i+1)+'/hsa/quote')
            total += str(BeautifulSoup(html))
        
        stock = {}
        stock_pri = pattern1.findall(total)
        for s in stock_pri:
            stockcode = pattern4.findall(pattern3.findall(s)[0])[0]
            stock[stockcode] = {}
            stock_0 = s.split(',')
            for Ele in stock_0[:-1]:
                if Ele.__contains__('"stockname') :
                    continue
                bre = Ele.split('":"')
                stock[stockcode][self.fnn(bre[0].split('"'))] = self.fnn(bre[1].split('"'))
        code = [i for i in stock]
        self.stock = stock
        return code, stock

#设定股票记录的初始日期，请选择要开始记录数据的前一天运行init，并初始化股票的编号（使用MySQLdb，请修改相应passwd）  
    def init(self):
        fp1 = open(self.path+'/original_time.txt', 'w')
        fp2 = open(self.path+'/log.txt', 'w')
        tm = time.localtime(time.time() + 24*60*60)
        dateC=datetime.datetime(tm.tm_year,tm.tm_mon,tm.tm_mday,9,30,0)
        timestamp=time.mktime(dateC.timetuple())
        fp1.write(str(timestamp))
        fp1.close()
        fp2.close()
        
        conn = MySQLdb.connect(host='localhost',user='root',passwd='1994hyde05MySQL20',port=3306)
        cur = conn.cursor()
        try:
            cur.execute('create database stock')
            conn.select_db('stock')
        except:
            conn.select_db('stock')
        try:
            cur.execute('drop table stockInfo')
            cur.execute('create table stockInfo(cje float(10,2),cjl float(10,1),hsl float(10,5),jk float(10,2),jlr float(10,2),code varchar(6),id varchar(5),zde float(5,2),zdf float(5,2),zs float(10,2),zxj float(10,2),No int)')
        except:
            cur.execute('create table stockInfo(cje float(10,2),cjl float(10,1),hsl float(10,5),jk float(10,2),jlr float(10,2),code varchar(6),id varchar(5),zde float(5,2),zdf float(5,2),zs float(10,2),zxj float(10,2),No int)')
        try:
            cur.execute('drop table stockcode')
            cur.execute('create table stockcode(code varchar(6))')
        except:
            cur.execute('create table stockcode(code varchar(6))')
        cur.executemany('insert into stockcode values(%s)', sorted(self.surf()[0]))
        conn.commit()
        cur.close()
        conn.close()
        
    def renew(self):
        conn = MySQLdb.connect(host='localhost',user='root',passwd='1994hyde05MySQL20',port=3306)
        cur = conn.cursor()
        conn.select_db('stock')
        code_o = [i[0] for i in cur.fetchmany(cur.execute('select * from stockcode'))]
        code_n, stock = self.surf()
        if sorted(code_o) != sorted(code_n):
            cur.executemany('insert into stockcode values(%s)', sorted([i for i in code_n if i not in code_o]))
            fp = open(self.path+'/log.txt', 'a')
            for i in [i for i in code_n if i not in code_o]:
                fp.write('Add new stock! The code is : ' + i +'\n')
            fp.close()
            
        No = self.num()
        insert = []
        for s in stock:
            insert_ = []
            insert_ += [float(stock[s][i]) for i in ['cje', 'cjl', 'hsl', 'jk', 'jlr']]
            insert_ += [stock[s][i] for i in ['stockcode', 'stockid']]
            insert_ += [float(stock[s][i]) for i in ['zde', 'zdf', 'zs', 'zxj']]
            insert.append(insert_ + [No])
        cur.executemany('insert into stockInfo values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', insert)
        conn.commit()
        cur.close()
        conn.close()
