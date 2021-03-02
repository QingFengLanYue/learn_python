import pandas as pd
file_path='D:/work2/朝阳医院2018年销售数据.xlsx'
salesDf = pd.read_excel(file_path, type=str)

# print(salesDf.loc[0:4,['购药时间','销售数量']])
#
colNameDict = {'购药时间':'销售时间','社保卡号':'卡号'}                  #将‘购药时间’改为‘销售时间’
salesDf.rename(columns = colNameDict,inplace=True)
# print(salesDf.head())


print('删除缺失值前大小',salesDf.shape)
salesDf=salesDf.dropna(subset=['销售时间','卡号'],how='any') #删除列（销售时间，社保卡号）中为空的行
print('删除缺失后大小',salesDf.shape)

print('转换前的数据类型：\n',salesDf.dtypes)
salesDf['销售数量'] = salesDf['销售数量'].astype('int')
salesDf['应收金额'] = salesDf['应收金额'].astype('float')
salesDf['实收金额'] = salesDf['实收金额'].astype('float')
print('转换后的数据类型：\n',salesDf.dtypes)




def splitSaletime(timeColSer):
    timeList = []
    for value in timeColSer:  # 例如2018-01-01 星期五，分割后为：2018-01-01
        dateStr = value.split(' ')[0]
        timeList.append(dateStr)

    timeSer = pd.Series(timeList)  # 将列表转行为一维数据Series类型
    return timeSer

timeSer=salesDf['销售时间']    #获取“销售时间”这一列
dateSer=splitSaletime(timeSer)      #对字符串进行分割，获取销售日期

salesDf['销售时间']=dateSer    #修改销售时间这一列的值
print(salesDf.head())

salesDf.loc[:,'销售时间']=pd.to_datetime(salesDf.loc[:,'销售时间'],
                                    format='%Y-%m-%d',
                                    errors='coerce')
salesDf=salesDf.dropna(subset=['销售时间','卡号'],how='any')


print(salesDf.head())

print('转换后的数据类型：\n',salesDf.dtypes)

print('排序前的数据集')
print(salesDf.head())
salesDf=salesDf.sort_values(by='销售时间',     #按销售日期进行升序排列
                    ascending=True)

print('排序后的数据集')
print(salesDf.head())
print(salesDf.describe())


#设置查询条件
querySer=salesDf.loc[:,'销售数量']>0
#应用查询条件
print('删除异常值前：',salesDf.shape)
salesDf=salesDf[querySer]
print('删除异常值后：',salesDf.shape)

#print('删除异常值前：',salesDf['销售数量']<0)
print(salesDf.describe())


kpi1_Df=salesDf.drop_duplicates(
    subset=['销售时间', '卡号']
)

totalI=kpi1_Df.shape[0]             #总消费次数————有多少行

print('总消费次数=',totalI)

#第1步：按销售时间升序排序
kpi1_Df=kpi1_Df.sort_values(by='销售时间',
                    ascending=True)
kpi1_Df=kpi1_Df.reset_index(drop=True)     #重命名行名（index）

#第2步：获取时间范围
startTime=kpi1_Df.loc[0,'销售时间']         #最小时间值
endTime=kpi1_Df.loc[totalI-1,'销售时间']    #最大时间值

#第3步：计算月份数
daysI=(endTime-startTime).days             #天数
monthsI=daysI//30                          #月份数: 运算符“//”表示取整除，返回商的整数部分，例如9//2 输出结果是4
print('月份数：',monthsI)

kpi1_I=totalI // monthsI
print('业务指标1：月均消费次数=',kpi1_I)

totalMoneyF=salesDf.loc[:,'实收金额'].sum()   #总消费金额
monthMoneyF=totalMoneyF / monthsI            #月均消费金额
print('业务指标2：月均消费金额= %0.2f'%monthMoneyF)

pct=totalMoneyF / totalI
print('客单价：%0.2f'%pct)

#在进行操作之前，先把数据复制到另一个数据框中，防止对之前清洗后的数据框造成影响
groupDf=salesDf

#第1步：重命名行名（index）为销售时间所在列的值
groupDf.index=groupDf['销售时间']

#第2步：分组
gb=groupDf.groupby(groupDf.index.month)

#第3步：应用函数，计算每个月的消费总额
mounthDf=gb.sum()

print(mounthDf.loc[0,'销售时间'] )