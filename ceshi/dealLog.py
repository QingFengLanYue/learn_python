import re
import os

import numpy as np

# file='D:/work2/cc.log'
# with open(file,mode='r',encoding='UTF-8') as f:
#     lines=str(f.readlines())
#     pattern1 = re.compile('总花费为：(\d+)')
#     pattern2 = re.compile('总奖金为：(\d+)')
#     pattern3 = re.compile('回报率为:(\d+.?\d+)')
#     m1 = re.findall(pattern1,lines)
#     m2 = re.findall(pattern2,lines)
#     m3 = re.findall(pattern3,lines)
#     m1 = list(map(int, m1))
#     m2 = list(map(int, m2))
#     m3 = list(map(float, m3))
#     total_m1=sum(m1)
#     total_m2=sum(m2)
#     syl=round(total_m2/total_m1*100,2)
#     print('总奖金为:%s,总花费为:%s,收益率为:%s%%'%(total_m2,total_m1,syl))
#
#     arr = np.array(m3)
#     arr1 = arr[arr >= syl]
#     arr2 = arr1[ (arr1 >= 1300) & (arr1 <= 1550)]
#     arr3 = arr1[ arr1 > 1550]
#     sec = len(arr2)
#     fir = len(arr3)
#     #print(sorted(arr1))
#     print('截至目前二等奖的数量为:%s,一等奖的数量为:%s'%(sec,fir))
import pandas as pd
from matplotlib import pyplot as plt

csv_file = 'D:/work2/cc_analy.csv'
columns=['次数','中奖号码','购买次数','一等奖','二等奖','三等奖','四等奖','五等奖','六等奖', '总花费', '总收益','回报率']




# df = pd.read_csv(csv_file,names=columns)
# print(df.head(1).T)
#
# h1=df['总花费'].sum()
# h2=df['总收益'].sum()
#
# h3=h2/h1

# print(h1,h2,h3)


# print(df['二等奖'].sum())
# print(df['总花费'].sum())
# print('回报率为:%.2f%%' % (df['总收益'].sum()/df['总花费'].sum()*100))

total_h = 0
total_s = 0
i = 0
x = []
y = []
y_t = []
j_1 = []
j_2 = []
j_3 = []
df = pd.read_csv(csv_file,names=columns,chunksize=100)
for chunk in df:
    i += len(chunk)
    x1 = chunk['总花费'].sum()

    js_1 = chunk['一等奖'].sum()
    js_2 = chunk['二等奖'].sum()
    js_3 = chunk['三等奖'].sum()


    total_h += x1
    x2 = chunk['总收益'].sum()
    total_s += x2
    x3 = x2 / x1 * 100

    x4 = total_s/total_h*100

    x.append(i)
    y.append(x3)
    y_t.append(x4)

    j_1.append(js_1)
    j_2.append(js_2)
    j_3.append(js_3)

plt.figure(1)
plt.subplot(1, 2, 1)
plt.xlabel("num")#x轴上的名字
plt.ylabel("money")#y轴上的名字

plt.plot(x, y, label="this period")
plt.plot(x, y_t, label="arv")
plt.legend(loc='upper left', bbox_to_anchor=(0.2, 0.95))

#用setp方法可以同时设置多个线条的属性

plt.figure(1)
plt.subplot(1, 2, 2)
plt.xlabel("num")#x轴上的名字
plt.ylabel("j_num")#y轴上的名字

plt.plot(x, j_1, label="first")
plt.plot(x, j_2, label="second" )
plt.plot(x, j_3, label="third")
plt.legend(loc='upper left', bbox_to_anchor=(0.2, 0.95))

plt.show()