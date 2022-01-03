"""
author:cai
project:learn_python
date:2021/12/29
"""
# coding=utf8
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


def great_number_concat(a):
    m = '2000000000000'
    if len(a) < 13:
        return m[0:13 - len(a)] + a
    else:
        return a[0:13]


def great_number(num):
    hotel = read_property()
    res = num.merge(hotel, how='left', left_on='chtl_code', right_on='dr3_hotel_code')
    res['id'] = res['id'].fillna('999')
    res['great_number'] = res['id'].str.cat(res['defecttrack_detailid'])
    res['great_number'] = res['great_number'].apply(great_number_concat)

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


def category_concat(data, category):
    category = data.merge(category, how='left', left_on=['question', 'sub_que', 'sub_sque'],
                          right_on=['QUESTION', 'SUB_QUE', 'SUB_SQUE'])
    return category[['Category 1', 'Category 2', 'New department responsible', 'New location']]


def mast_category(data, category):
    master_category = data.merge(category, how='left', left_on=['Category 2', 'Category 1', 'property_code'],
                                 right_on=['category_item', 'category_type', 'property_code'])
    master_category['category_code'] = master_category['category_code'].fillna('error code 06')
    return master_category[['category_code', 'category_type', 'category_item']]


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
    print(data)
    print(data.shape[0])

    m = cur.fetchmany(3)
    print("下一批")
