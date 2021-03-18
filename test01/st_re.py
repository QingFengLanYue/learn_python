#mysql 连接
import datetime
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
    sql="select * from %s limit 500"%(table)
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

    return date,pms_amt,cen_amt,pms_cur,cen_cur,exc


def dict_deal(dict1,list1):
    dict2={}
    for key,value in dict1.items():

        val = list1.get(value,None)
        dict2[key] = val
    return dict2

def dict_reve():
    dict1={'date' : 'date',
        'pms_amt' : 'pmsRateAmt',
        'cen_amt' : 'centralRateAmt',
        'pms_cur' : 'pmsCurrency',
        'cen_cur': 'centralCurrency',
        'rev_type':'revenueType',
        'exc' : 'exchange',
        'de' : 'deleteFlag',
        'seq' : 'seq'
        }
    return dict1


def dict_rate():
    dict1= {'begin_date':"fromDate",
            'end_date':"toDate",
            'rate_code':"rateCode",
            'market_code':"marketCode"
        }
    return dict1

def rate_deal(stay_record_id,dict1,rate_list):
    dict3 = dict_deal(dict1, rate_list)
    begin_date = dict3['begin_date']
    end_date = dict3['end_date']
    rate_code = dict3['rate_code']
    market_code = dict3['market_code']

    l1 = [stay_record_id, begin_date, end_date, rate_code, market_code]
    return l1

def reve_deal(stay_record_id,pms_conf_no,dict1,reve_list):
    dict3 = dict_deal(dict1, reve_list)
    date = dict3['date']
    pms_amt = dict3['pms_amt']
    cen_amt = dict3['cen_amt']
    pms_cur = dict3['pms_cur']
    cen_cur = dict3['cen_cur']
    rev_type = dict3['rev_type']
    exc = dict3['exc']
    de = dict3['de']
    seq = dict3['seq']
    l1 = [stay_record_id, pms_conf_no, date, pms_amt, cen_amt, pms_cur, \
          cen_cur, rev_type, exc, de, seq]
    return l1

def date_deal(l):

    stay_record_id = l[0]
    begin_date = datetime.datetime.strptime(l[1], "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(l[2], "%Y-%m-%d").date()
    rate_code = l[3]
    market_code = l[4]
    res = []
    if begin_date == end_date:
        date = str(begin_date)
        l=[stay_record_id,date,rate_code,market_code]
        res.append(l)
    else :
        date1 = []
        while begin_date <= end_date:
            date1.append(str(begin_date))
            begin_date = begin_date + datetime.timedelta(days=1)

        for date in date1:
            l=[stay_record_id, date, rate_code, market_code]
            res.append(l)
    return res



def main(sql):

    #sql=select_sql(table_name)
    result=get_all(sql)
    l_res=[]
    l_rate=[]
    for i in result:
        stay_record_id=i[24]
        res1=i[2]
        #print(res1)
        res2=json.loads(res1)

        dict1 = dict_reve()
        dict2 = dict_rate()
        rev_list=res2['revenueList']
        rate_list=res2['rateList']
        #print(rev_list)
        pms_conf_no = res2['altIds'][0]['id']

        for n in range(len(rev_list)):
            l1 = reve_deal(stay_record_id,pms_conf_no,dict1,rev_list[n])
            l_res.append(l1)

        for m in range(len(rate_list)):
            l2 = rate_deal(stay_record_id,dict2,rate_list[m])
            res = date_deal(l2)

            l_rate.extend(res)


    df1 = pd.DataFrame(l_res, columns=['stay_record_id', 'pms_no', 'date', 'pms_amt', 'cen_amt', \
                                      'pms_cur', 'cen_cur', 'rev_type', 'exc', 'de', 'seq'])
    df2 = pd.DataFrame(l_rate,columns=['stay_record_id', 'date', 'rate_code', 'market_code'])

    return df1,df2


#print(l_res)

if __name__ == '__main__':

    sql = 'select * from stay_record_test where stay_record_id =2 '
    file = 'D:/work2/tmp/stay_rev.xlsx'
    writer = pd.ExcelWriter(file)
    df1, df2 = main(sql)
    df1.to_excel(writer, sheet_name='revenue', index=False)
    df2.to_excel(writer, sheet_name='rate', index=False)
    writer.save()