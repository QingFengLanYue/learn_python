import pymysql
import pandas as pd
import re
import functools
def cur_conn():
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='test', charset='utf8')
    cur = conn.cursor()
    return conn,cur

def decorate(func):
    def except_deal(sql):
        try:
            return func(sql)
        except pymysql.err.ProgrammingError as e:
            print('Sql 语句报错', e)
            # 捕获由于sql语句错误抛出的异常
            # 捕获后的操作
        except pymysql.err.IntegrityError as e:
            print('主键冲突,请核对后重新输入\n', e)

    return except_deal

@decorate
def conn_mysql_select(sql):
    # conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='test', charset='utf8')
    # cur = conn.cursor()
    conn,cur = cur_conn()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

@decorate
def conn_mysql_insert(sql):
    # conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='test', charset='utf8')
    # cur = conn.cursor()
    conn,cur = cur_conn()
    cur.execute(sql)
    cur.execute('commit')
    cur.close()
    conn.close()







sql1='select * from test.daily_revenue'
re1=conn_mysql_select(sql1)

sql2='select * from test.stay_record'
re2=conn_mysql_select(sql2)

df_tab1=pd.DataFrame(re2,columns=['id','name','trx_date'])




df=pd.DataFrame(re1,columns=['id','type','revenue'])
df['detial']='['+df['type']+','+df['revenue']+']'

df2=df[['id','detial']]

df3=df.groupby('id')['detial'].apply(lambda x:x.str.cat(sep=','))
#df3['detial1']='{detial:'+df3['detial']+'}'

#df4=pd.DataFrame(df3)

# print(df3)
#
# print(df_tab1)
df4=pd.merge(df_tab1,df3,on=["id","id"],how='left')
df4['detial2']='detial_list{'+df4['detial']+'}'
df5=df4[['id','name','detial2']].values
# for i in range(2):
#     print(df5[i])

num=df5.shape[0]
for i in range(num):
    a=df5[i]
    b=str(a).replace(' ',',').replace('[','(').replace(']',')')
    sql='insert into test.cs_01(id,name,detial) values' +b
    print(sql)


    conn_mysql_insert(sql)
    # try:
    #     conn_mysql_insert(sql)
    # except pymysql.err.ProgrammingError as e:
    #     print('Sql 语句报错',e)
    # # 捕获由于sql语句错误抛出的异常
    # # 捕获后的操作
    # except pymysql.err.IntegrityError as e:
    #     print('主键冲突',e)
# 捕获主键冲突
# 捕获后的相关操作




#coding=utf-8
import numpy as np
import pandas as pd


def merge():
    """
    merge使用
    :return:
    """
    data1 = pd.DataFrame(np.arange(24).reshape(4,6),columns=list("abcdef"))
    data2 = pd.DataFrame(np.arange(24).reshape(4,6),columns=list("avwxyz"))
    data1.iloc[2,0] = 100
    print(data1)
    print(data2)

    #inner连接 ,选取两边都存在的值，即取交集
    print(pd.merge(data1,data2,on=["a","a"]))

    # 右连接，以data2为主表，如果data1表中没有data2对应的数据，则置为NaN
    print(pd.merge(data1,data2,on=["a","a"],how="right"))


    data1 = pd.DataFrame(np.arange(24).reshape(4,6),columns=list("abcdef"))
    data2 = pd.DataFrame(np.arange(24).reshape(4,6),columns=list("qvwxyz"))
    data1.iloc[2,0] = 100
    print(data1)
    print(data2)

    #如果两个表的列名称不对应，则使用left_on 与right_on一起使用，两个必须一起使用，反之，如果列名对应，则使用on
    print(pd.merge(data1,data2,left_on=["a"],right_on=["q"])) #左表以"a"作为连接主键，右表以"q"连接

    return None


def join():
    """
    join使用:行合并
        如果存在相同的列名，则不能使用，只能使用merge
    :return:
    """
    data1 = pd.DataFrame(np.arange(24).reshape(4, 6), columns=list("abcdef"))
    data2 = pd.DataFrame(np.arange(12).reshape(3, 4), columns=list("wxyz"))
    data1.iloc[3,0]=100
    print(data1)
    print(data2)
    print(data1.join(data2)) #直接将两个数据进行行添加
    print(data1.join(data2,how="right")) #以右表为主连接表
    print(data1.join(data2, how="left")) #以左表为主连接表
    return None


def concat():
    """
    concat使用:全连接方式
    :return:
    """
    data1 = pd.DataFrame(np.arange(24).reshape(4, 6), columns=list("abcdef"))
    data2 = pd.DataFrame(np.arange(12).reshape(3, 4), columns=list("wxyz"))
    data1.iloc[3, 0] = 100
    print(data1)
    print(data2)
    frame = [data1,data2]
    print(pd.concat(frame)) #全连接

    #print(pd.concat(frame,keys=["h","i"])) #指定行索引

    return None

if __name__ == '__main__':
    #merge()
    #join()
    #concat()
    pass
