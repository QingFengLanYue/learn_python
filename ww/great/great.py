"""
author:cai
project:learn_python
date:2021/12/29
"""
# coding=utf8
import datetime
import re
import sqlite3
import uuid

import pandas as pd
from ww.great import data_ready

con = sqlite3.connect("test.db")
cur = con.cursor()
hh = con.cursor()
column_list = data_ready.table_list()

cur.execute("select * from detail")
m = cur.fetchmany(3)


def uuid_version():
    uuidOne = uuid.uuid1()
    uuidOne = re.sub('-', '', str(uuidOne))
    return uuidOne


def uuid_list(num):
    ul = []
    for i in range(num):
        l = uuid_version()
        ul.append(l)
    return ul


def main_deal(x):
    x = tuple(x)
    x = re.sub(',\)', ')', str(x))
    main_sql = f"select * from main where defecttrack_mainid in {x}"
    hh.execute(main_sql)
    main = pd.DataFrame(hh.fetchall(), columns=column_list.get('main'))
    return main


def read_property():
    property_column = ['id', 'dr3_hotel_code', 's_hotel_code']
    # with open('property.txt', mode="r") as f:
    #     print(f.readlines())
    #     # m = pd.DataFrame(f.readlines(),columns=property_column)
    m = pd.read_csv('data/property.txt', delimiter='!#~', dtype=str, header=None, engine='python')
    m.columns = property_column
    return m


def number_concat(a, m):
    # m = '2000000000000'
    l = len(m)
    if len(a) < l:

        return m[0:l - len(a)] + a
    else:
        return a[0:l]


def great_number(num):
    hotel = read_property()
    res = num.merge(hotel, how='left', left_on='chtl_code', right_on='dr3_hotel_code')
    res['id'] = res['id'].fillna('999')
    res['great_number'] = res['id'].str.cat(res['defecttrack_detailid'])
    res['great_number'] = res['great_number'].apply(number_concat, args=('2000000000000',))

    return res['great_number'], res['s_hotel_code'].fillna('error code 01')


def category_read():
    file = 'data/Category Mapping.xlsx'
    h = pd.read_excel(file, sheet_name='Sheet1')
    h = h.fillna(method='pad')
    return h


def mast_category_read():
    property_column = ['id', 'category_code', 'category_type', 'category_item', 'property_code', 'language_code',
                       'default_department_code', 'is_deleted', 'create_by', 'create_time', 'update_by', 'update_time']
    m = pd.read_csv('data/master_category.txt', delimiter='!#~', dtype=str, header=None, engine='python')
    m.columns = property_column
    return m


def location_read():
    property_column = ['id', 'location_id', 'node_type', 'node_code', 'parent_id', 'property_code']
    m = pd.read_csv('data/localtion.txt', delimiter='!#~', dtype=str, header=None, engine='python')
    m.columns = property_column
    return m


def department():
    property_column = ['id', 'department_code', 'department_name', 'department_level', 'parent_department_code',
                       'is_deleted', 'create_by', 'create_time', 'update_by', 'update_time']
    m = pd.read_csv('data/department.txt', delimiter='!#~', dtype=str, header=None, engine='python')
    m.columns = property_column
    m = m[m['department_level'] == 2]
    return m


def department_concat(data, department):
    department = data.merge(department, how='left', left_on='New department responsible',
                            right_on='department_name')
    return department['department_code']


def code_check(df1, column, st1, column1, column2):
    if df1[column] == st1:
        return df1[column1]
    else:
        return df1[column2]


def localtion_deal(data):
    l = location_read()
    data = data[['New location', 'nroom_no', 'property_code']]
    m = pd.merge(data, l, how='left', left_on=['nroom_no', 'property_code'], right_on=['node_code', 'property_code'])
    m['no_01'] = m['node_code'].fillna('error code 15')

    m = pd.merge(m, l, how='left', left_on=['New location', 'property_code'],
                 right_on=['node_code', 'property_code'])

    m['node_code_n'] = m['node_code_y'].fillna('error code 14')
    m['s_node_code'] = m.apply(code_check, args=('New location', 'Guest room <#>', 'no_01', 'node_code_n'),
                               axis=1)
    return m['s_node_code']


def category_concat(data, category):
    category = data.merge(category, how='left', left_on=['question', 'sub_que', 'sub_sque'],
                          right_on=['QUESTION', 'SUB_QUE', 'SUB_SQUE'])
    return category[['Category 1', 'Category 2', 'New department responsible', 'New location']]


def mast_category(data, category):
    master_category = data.merge(category, how='left', left_on=['Category 2', 'Category 1', 'property_code'],
                                 right_on=['category_item', 'category_type', 'property_code'])
    master_category['category_code'] = master_category['category_code'].fillna('error code 06')
    return master_category[['category_code', 'category_type', 'category_item']]


def read_ad():
    df = pd.read_csv('data/ad.csv', dtype=str)
    return df


def read_user():
    df = pd.read_csv('data/user.csv', dtype=str)
    return df


def user_name(n):
    if n['ad'] == 'both' and n['s_360'] == 'both':
        return n['s_name']
    elif n['ad'] == 'both' and n['s_360'] == 'left_only':
        return 'error code 08'
    else:
        return 'error code 09'


def report_by_deal(res, col):
    ad = read_ad()
    user = read_user()
    user['s_name'] = user['user_name']
    res[col] = res[col].fillna('user4.test@sl.net')
    r1 = pd.merge(res, ad, how='left', left_on=col, right_on='user_name', indicator='ad')
    r1['user_name'] = r1['user_name'].fillna('error code 09')
    # print(r1)
    r2 = pd.merge(r1, user, how='left', on='user_name', indicator='s_360')
    r2['s_name'] = r2['s_name'].fillna('error code 08')
    r2['s_name'] = r2.apply(user_name, axis=1)
    return r2['s_name']


def s_status():
    status = {'N': '0', 'F': '1', 'P': '1'}
    return status


def s_resovled_by():
    if res['cresolution'] != 'N':
        return report_by_deal(res, 'reported_by')


while m:
    data = pd.DataFrame()
    table_detail = pd.DataFrame(m, columns=column_list.get('detail'))
    mainid = table_detail['defecttrack_mainid']
    main = main_deal(mainid)
    res = pd.merge(table_detail, main, on=['chtl_code', 'defecttrack_mainid'], suffixes=['_detail', '_main'])
    greatno = res[['chtl_code', 'defecttrack_detailid']]
    data['great_number'], data['property_code'] = great_number(greatno)

    category = category_read()
    m = category_concat(res, category)
    data = pd.concat([data, m], axis=1)
    mastcate = mast_category_read()
    mcat = mast_category(data, mastcate)
    data = pd.concat([data, mcat], axis=1)
    data['version'] = uuid_list(data.shape[0])
    data['date_feedback_received'] = res['drec_date_detail'].fillna('error code 02')
    data['narrative'] = res['comment'].fillna('N/A')

    data['report_by'] = report_by_deal(res, 'reported_by')
    data['report_by_name'] = data['report_by'].fillna('user4 test')

    data['nroom_no'] = res['nroom_no'].apply(number_concat, args=('0000',))

    # pd.set_option('display.height', 1000)
    # pd.set_option('display.max_rows', 500)
    # pd.set_option('display.max_columns', 500)
    # pd.set_option('display.width', 1000)

    data['node_code'] = localtion_deal(data)
    data['actual_defect_date'] = res['dact_date_detail'].apply(
        lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    data['status'] = res['cresolution'].map(s_status()).fillna('2')
    data['meal_period_id'] = None
    data['resovled_by'] = data.apply(code_check, args=('status', 'N', 'report_by', 'meal_period_id'), axis=1)
    data['resovled_by_name'] = data.apply(code_check, args=('status', 'N', 'report_by_name', 'meal_period_id'), axis=1)
    data['service_recovery_provided'] = res['resol_narrative']
    data['service_recovery_provided'] = data.apply(code_check, args=('status', 'N', 'service_recovery_provided',
                                                                     'meal_period_id'), axis=1).fillna('N/A')
    data['compensation_id'] = '0'
    data['responsible_department_code'] = department_concat(data, department()).fillna('error code 12')

    data[['charge_to_department_code', 'root_cause_id', 'root_cause_detail', 'check_in_order_number']] = None

    print(data)

    m = cur.fetchmany(3)
    print("下一批")
