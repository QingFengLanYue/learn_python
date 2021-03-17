#mysql 连接
import json

import pymysql

import pandas as pd


def con_my():
    host='localhost'
    port=3306
    user='root'
    password='root'
    db='test'
    conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8')
    cur = conn.cursor()
    return conn,cur


def select_sql(table):
    sql="select * from %s limit 100"%(table)
    return sql



def get_all(sql):
    conn,cur = con_my()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

def rev_list_deal(rev_list ) :
    date = rev_list['date']
    pms_amt = rev_list['pmsRateAmt']
    cen_amt = rev_list['centralRateAmt']
    pms_cur = rev_list['pmsCurrency']
    cen_cur = rev_list['centralCurrency']
    exc = rev_list['exchange']
    if not rev_list['deleteFlag']:
        de = 1
    else:
        de =  rev_list['deleteFlag']
    return date,pms_amt,cen_amt,pms_cur,cen_cur,exc,de


sql=select_sql('stay_record_01')
result=get_all(sql)
for i in result:
    stay_record_id=i[24]
    res1=i[2]
    #print(res1)
    res2=json.loads(res1)






    rev_list=res2['revenueList']
    #print(rev_list)
    for n in range(len(rev_list)):
        date, pms_amt, cen_amt, pms_cur, cen_cur, exc, de = rev_list_deal(rev_list[n])
        print(stay_record_id, res2['altIds'][0]['id'],date, pms_amt, cen_amt, pms_cur, cen_cur, exc)

