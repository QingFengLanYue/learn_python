#-*- coding:utf-8 -*-
import numpy as np
import pandas as pd
from openpyxl.workbook import Workbook


sheet_name = 'DWD_MARKET_DIM'
df = pd.read_excel(r'C:\Users\HP\Desktop\数据测试.xlsx',sheet_name='Sheet1')
#print(df)
a = df.values
#print(a)
a = a[a[:, 7] > a[:, 8]]
data_df = pd.DataFrame(a)
data_df.columns = ['单据号', '商品编码', '商品售价', '销售数量', '消费金额', '消费产生的时间', '收银机号', '实际收费', '消费金额']

data_df.index = range(10)
#print(data_df)

writer = pd.ExcelWriter(r'C:\Users\HP\Desktop\ret.xlsx')
data_df.to_excel(writer,sheet_name='sheet3')
data_df.to_excel(writer,sheet_name='sheet4')
writer.save()

df2=pd.read_excel(r'C:\Users\HP\Desktop\ret.xlsx',sheet_name='sheet3')
print(df2.ix[:,[2,3,4]])
