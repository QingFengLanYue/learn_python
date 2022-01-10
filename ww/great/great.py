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

con = sqlite3.connect("test.db")
cur = con.cursor()
hh = con.cursor()

cur.execute("select * from detail")
m = cur.fetchmany(3)


class ReadData:
    def __init__(self, file_name, **kwargs):
        self.file_name = 'data/' + file_name
        self.sep = kwargs.get('sep', False)
        self.columns = kwargs.get('columns', False)

    def read_txt(self):
        reader = pd.read_csv(self.file_name, sep=self.sep, dtype=str, header=None, engine='python')
        reader.columns = self.columns
        return reader

    def read_csv(self):
        reader = pd.read_csv(self.file_name, dtype=str)
        return reader

    def read_excel(self):
        reader = pd.read_excel(self.file_name, sheet_name='Sheet1')
        reader = reader.fillna(method='pad')
        return reader

    def read_database(self):
        pass

    def read_check(self):
        if self.file_name.endswith('.txt'):
            return self.read_txt()
        elif self.file_name.endswith('.csv'):
            return self.read_csv()
        elif self.file_name.endswith('.xlsx'):
            return self.read_excel()


def file_deal(file_name, sep=None, columns=None):
    read = ReadData(file_name, sep=sep, columns=columns)
    return read.read_check()


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
    colnames = [desc[0] for desc in hh.description]
    main = pd.DataFrame(hh.fetchall(), columns=colnames)
    return main


def read_property():
    columns = ['id', 'dr3_hotel_code', 's_hotel_code']
    m = file_deal('property.txt', '!#~', columns)
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


# def category_read():
#     file = 'Category Mapping.xlsx'
#     h = file_deal('Category Mapping.xlsx')
#     return h


def mast_category_read():
    columns = ['id', 'category_code', 'category_type', 'category_item', 'property_code', 'language_code',
               'default_department_code', 'is_deleted', 'create_by', 'create_time', 'update_by', 'update_time']
    # m = pd.read_csv('data/master_category.txt', delimiter='!#~', dtype=str, header=None, engine='python')
    # m.columns = property_column
    m = file_deal('master_category.txt', '!#~', columns)
    return m


def location_read():
    columns = ['id', 'location_id', 'node_type', 'node_code', 'parent_id', 'property_code']
    m = file_deal('localtion.txt', '!#~', columns)
    return m


def department():
    columns = ['id', 'department_code', 'department_name', 'department_level', 'parent_department_code',
               'is_deleted', 'create_by', 'create_time', 'update_by', 'update_time']
    m = file_deal('department.txt', '!#~', columns)
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


# def read_ad():
#     df = file_deal('ad.csv')
#     return df

#
# def read_user():
#     df = file_deal('user.csv')
#     return df


def user_name(n, ec1, ec2):
    if n['ad'] == 'both' and n['s_360'] == 'both':
        return n['s_name']
    elif n['ad'] == 'both' and n['s_360'] == 'left_only':
        return ec1
    else:
        return ec2


def report_by_deal(res, col, ec1, ec2):
    ad = file_deal('ad.csv')
    user = file_deal('user.csv')
    user['s_name'] = user['user_name']
    res[col] = res[col].fillna('user4.test@sl.net')
    r1 = pd.merge(res, ad, how='left', left_on=col, right_on='user_name', indicator='ad')
    r1['user_name'] = r1['user_name'].fillna(ec2)
    # print(r1)
    r2 = pd.merge(r1, user, how='left', on='user_name', indicator='s_360')
    r2['s_name'] = r2['s_name'].fillna(ec1)
    r2['s_name'] = r2.apply(user_name, args=(ec1, ec2), axis=1)
    return r2['s_name']


def s_status():
    status = {'N': '0', 'F': '1', 'P': '1'}
    return status


def s_resovled_by():
    if res['cresolution'] != 'N':
        return report_by_deal(res, 'reported_by')


def datetime_concat(x, y):
    x = x.split()[0]
    z = datetime.datetime.strptime(x + ' ' + y, '%Y-%m-%d %I:%M:%S %p')
    return z


def mast_source_reed():
    columns = ['id', 'source_code', 'language_code', 'is_deleted', 'create_by', 'create_time', 'update_by',
               'update_time']
    m = file_deal('mast_source.txt', '\|\|', columns)
    return m


# def source_read():
#     file = 'Souce Mapping.xlsx'
#     h = file_deal('Souce Mapping.xlsx')
#     return h


def source_id_deal(data):
    mast_source = mast_source_reed()
    source = file_deal('Souce Mapping.xlsx')
    source_code = data.merge(source, how='left', left_on='csource_detail', right_on='Old Sources Mapped in')
    source_id = pd.merge(source_code, mast_source, how='left', left_on='New Proposed Sources', right_on='source_code')
    return source_id['id']


while m:
    data = pd.DataFrame()
    columns = [desc[0] for desc in cur.description]
    table_detail = pd.DataFrame(m, columns=columns)
    mainid = table_detail['defecttrack_mainid']
    main = main_deal(mainid)
    res = pd.merge(table_detail, main, on=['chtl_code', 'defecttrack_mainid'], suffixes=['_detail', '_main'])
    greatno = res[['chtl_code', 'defecttrack_detailid']]
    data['great_number'], data['property_code'] = great_number(greatno)
    source_id = source_id_deal(res)
    data = pd.concat([data, source_id], axis=1)

    category = file_deal('Category Mapping.xlsx')
    m = category_concat(res, category)
    data = pd.concat([data, m], axis=1)
    mastcate = mast_category_read()
    mcat = mast_category(data, mastcate)
    data = pd.concat([data, mcat], axis=1)
    data['version'] = uuid_list(data.shape[0])
    data['date_feedback_received'] = res['drec_date_detail'].fillna('error code 02')
    data['narrative'] = res['comment'].fillna('N/A')

    data['report_by'] = report_by_deal(res, 'reported_by', 'error code 08', 'error code 09')
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
    data['resovled_by'] = data.apply(code_check, args=('status', '0', 'report_by', 'meal_period_id'), axis=1)
    data['resovled_by_name'] = data.apply(code_check, args=('status', 'N', 'report_by_name', 'meal_period_id'), axis=1)
    data['service_recovery_provided'] = res['resol_narrative']
    data['service_recovery_provided'] = data.apply(code_check, args=('status', '0', 'service_recovery_provided',
                                                                     'meal_period_id'), axis=1).fillna('N/A')
    data['compensation_id'] = '0'
    data['responsible_department_code'] = department_concat(data, department()).fillna('error code 12')

    data[['charge_to_department_code', 'root_cause_id', 'root_cause_detail', 'check_in_order_number']] = None

    data['update_time'] = res.apply(lambda x: datetime_concat(x['cup_date_detail'], x['cup_time_detail']), axis=1)
    data['resovled_time'] = data.apply(code_check, args=('status', '0', 'meal_period_id', 'update_time'), axis=1)
    data['closed_time'] = data.apply(code_check, args=('status', '2', 'update_time', 'meal_period_id'), axis=1)
    data['cup_user'] = res['cup_user_detail']
    data['closed_by'] = data.apply(code_check, args=('status', '2', 'cup_user', 'meal_period_id'), axis=1)
    data[['is_deleted', 'great_source']] = 0, 2
    data['create_by'] = report_by_deal(res, 'ccre_user', 'error code 10', 'error code 11')
    data['create_time'] = res.apply(lambda x: datetime_concat(x['ccre_date'], x['ccre_time']), axis=1)
    data['defecttrack_mainid'] = res['defecttrack_mainid']
    data['defecttrack_detailid'] = res['defecttrack_detailid']
    data['cgcno'] = res['cgcno']
    data['cgst_fname'] = res['cgst_fname']
    data['cgst_lname'] = res['cgst_lname']
    data['cemail'] = res['cemail']
    data['camcmemberno'] = res['camcmemberno']
    data['resol_narrative'] = res['resol_narrative']
    data['ccre_date'] = res['ccre_date']

    # data.query('property_code != "error code 01" &  date_feedback_received != "error '
    #            'code 02" & actual_defect_date != "error code 03" & category_code != "error code 05" & category_code '
    #            '!= "error code 06" & responsible_department_code != "error code 12"')

    print('values' + str(data)+ ';')

    m = cur.fetchmany(3)
    print("下一批")
