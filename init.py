# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

import main

path= input('请输入存资料的文件路径,例('/home/hyde')')

s = main.stockdata(path)
s.init()
