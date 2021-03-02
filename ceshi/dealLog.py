import re
import os

import numpy as np

file='D:/work2/cc.log'
with open(file,mode='r',encoding='UTF-8') as f:
    lines=str(f.readlines())
    pattern1 = re.compile('总花费为：(\d+)')
    pattern2 = re.compile('总奖金为：(\d+)')
    pattern3 = re.compile('回报率为:(\d+.?\d+)')
    m1 = re.findall(pattern1,lines)
    m2 = re.findall(pattern2,lines)
    m3 = re.findall(pattern3,lines)
    m1 = list(map(int, m1))
    m2 = list(map(int, m2))
    m3 = list(map(float, m3))
    total_m1=sum(m1)
    total_m2=sum(m2)
    syl=round(total_m2/total_m1*100,2)
    print('总奖金为:%s,总花费为:%s,收益率为:%s%%'%(total_m2,total_m1,syl))

    arr = np.array(m3)
    arr1 = arr[arr >= syl]
    arr2 = arr1[ (arr1 >= 1300) & (arr1 <= 1550)]
    arr3 = arr1[ arr1 > 1550]
    sec = len(arr2)
    fir = len(arr3)
    #print(sorted(arr1))
    print('截至目前二等奖的数量为:%s,一等奖的数量为:%s'%(sec,fir))