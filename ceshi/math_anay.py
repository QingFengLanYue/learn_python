import re
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# file='D:/work2/cc.log'
# with open(file,mode='r',encoding='UTF-8') as f:
#     lines=str(f.readline())
#     pattern1 = re.compile('总花费为：(\d+)')
#     s1=re.findall(pattern1,lines)
#     print(s1)
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',300)

file='D:/work2/cc_test.log'
with open(file,mode='r',encoding='utf-8') as f:
    lines=str(f.readlines())
    pattern1 = re.compile('此次随机的奖号码为：\\[(\d+, \d+, \d+, \d+, \d+, \d+, \d+)')
    m1 = re.findall(pattern1,lines)

    l2=[]
    for i in m1:
        i = i.split(',')
        i = list(map(int, i))
        l2.append(i)

    df=pd.DataFrame(l2,columns=['red1','red2','red3','red4','red5','red6','blue'])

    print(df.mean())
    print(df.mean())#均值
    print(df.median())#中位数
    print(df.mode())#众数
    print(df.var())#方差
    print(df.std())#标准差
    print(df.mad())#平均绝对偏差
    print(df.skew())#偏度
    print(df.kurt())#峰度
    print(df.describe())#
    print(max(df['blue']))
    # df.plot.bar(stacked=True)
    # df.plot()
    # df.plot(kind='bar')
    # df.plot.barh(stacked=True)
    # df.plot.hist(bins=20)
    # df.hist(bins=20)
    #df.plot.box()
    #df.plot.area()
    #df.plot.kde()
    #df['blue'].plot()
    #df['blue'].rolling(10).mean().plot()
    #$df.plot.pie(subplots=True)
    #df.plot.scatter(x='red1', y='red2',c='red3',s=df['blue'] * 200)
    #df.plot.hexbin(x='red1', y='red6',gridsize=18)
    df.plot(subplots=True)

    plt.show()