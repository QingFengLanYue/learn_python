import datetime

import numpy as np
from impala.dbapi import connect
import pandas as pd


def hive_conn(hsql, num):
    conn = connect(host='0.0.0.0', port=10000, database='tmp', auth_mechanism='PLAIN')
    # print(cursor.description)  # prints the result set's schema
    res = pd.read_sql(hsql, conn, chunksize=num, parse_dates=['ccre_date', 'create_time'])
    return res


def date_format(s):
    if len(s) == 10:
        s = datetime.datetime.strptime(s, '%Y-%m-%d')
    elif len(s) == 19:
        s = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    s = s.strftime('%d-%b-%y')
    s = s.lstrip('0')
    return s


if __name__ == '__main__':
    file_name = 'GC Redemption Detail.csv'
    column = ['EARNING CREDIT DATE',
              'B360 CONF NO',
              'AWARD JOINT ID',
              'ISSUED AWARD ID',
              'MEMBERSHIP CARD NO',
              'MEMBERSHIP LEVEL',
              'AWARD ITEM',
              'POINTS',
              'POINTS VALUE',
              'RESORT',
              'REDEMPTION DATE',
              'CHECK IN',
              'CHECK OUT',
              'POSTING DATE',
              'TRX TYPE',
              'EARNING SOURCE',
              'EARNING ACTIVITIES',
              'ORIGINAL EXPIRY DATE',
              'REVISED EXPIRY DATE']
    df = pd.DataFrame(list(), columns=column)
    df.to_csv(file_name, index=False)
    sql = '''select  earning_credit_date, b360_conf_no, award_joint_id, issued_award_id, membership_no, 
    membership_level, award_item, points, points_value , property, redemption_date, arrival_date, departure_date, 
    posting_date , trx_type, earning_source, earning_activities, orig_expire_date, revised_expire_date  from 
    dwm.dwm_gc_redemption_detail_df d where dt='2022-01-17' and to_date(redemption_date) = '2022-01-17' limit  100000 
    '''
    r = hive_conn(sql, num=10000)
    for x in r:
        # m = [i.split('.')[1] for i in x.columns]
        # x.columns = m
        x['earning_credit_date'] = x['earning_credit_date'].apply(date_format)
        x['redemption_date'] = x['redemption_date'].apply(date_format)
        x['posting_date'] = x['posting_date'].apply(date_format)
        x['revised_expire_date'] = x['revised_expire_date'].apply(date_format)
        x['orig_expire_date'] = x['orig_expire_date'].apply(date_format)
        x = x.fillna('')
        x = x.astype(str)
        x.to_csv(file_name, mode='a', index=False, header=None)
