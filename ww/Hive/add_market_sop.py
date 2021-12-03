# coding=utf8
import re
import subprocess

import pandas as pd
import time
import datetime


def insert_sql(df):
    df1 = [tuple(xi) for xi in df.values]
    df2 = ','.join(str(x) for x in df1)
    return df2


def check_sql(df):
    df3 = [xi for xi in df.values]
    df4 = tuple(df3)
    return df4


def read_excel(file):
    df = pd.read_excel(file, )
    df = df[df['是否此次新增'].isin(['Y'])]
    df = df.drop(columns=['是否此次新增'])
    check_null = df[df.isnull().T.any()]
    if len(check_null) > 0:
        print('新增数据有空字段,无法入库!')
        print(check_null)
        exit(0)
    return df, df['Code代码']


def max_partition(table):
    cmd = """hive -e 'show partitions %s'""" % table
    (status, output) = run_shell(cmd)
    if status != 0:
        print('提取%s表分区失败' % table)
        return None
    r = re.findall('(\w+=[^\s]+)', output)
    r = list(map(lambda y: y.split('=')[1], r))
    if len(r) == 0:
        print(f"获取{table}分区失败")
        exit(1)
    return max(r)


def hive_sql(sql):
    cmd = f'hive -e "{sql}"'
    (status, output) = run_shell(cmd)
    if status != 0:
        print('sql:%s执行失败' % sql)
        return None
    return output


def run_shell(cmd):
    sub = subprocess.Popen(""" %s """ % cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='.', shell=True)
    outs = []
    while sub.poll() is None:
        lines = sub.stdout.readlines()
        lines = [line.decode('utf-8', 'ignore') for line in lines]
        outs = outs + lines
        time.sleep(1)
    return sub.returncode, ''.join(outs)


def add_code_desc(df):
    df['market_code_desc'] = ''
    return df


def sql_join(a):
    return a + 'b'


def sql_join2(a, b):
    return a + b


if __name__ == '__main__':
    excel_file = 'Dashboard_market segment_test.xlsx'

    table_list = ['edw.d_edw_rooms_market_ful',
                  'edw.d_edw_market_hotel',
                  # 'ods.d_ods_file_market_segment_ful',
                  # 'dws.dws_file_market_segment_df',
                  'cdm.d_cdm_otb_market_hotel']

    x1, market_code = read_excel(excel_file)

    # print(x2)
    sql1 = insert_sql(x1)
    x2 = add_code_desc(x1)
    sql2 = insert_sql(x2)
    market_check = check_sql(market_code)
    dt = max_partition('ods.d_ods_file_market_segment_ful')
    zz = [f"INSERT INTO TABLE {i} values {sql2};" for i in table_list]
    hh = [f"SELECT * FROM {i} WHERE market_code in {market_check};" for i in table_list]
    hh.append(f"SELECT * FROM ods.d_ods_file_market_segment_ful WHERE dt='{dt}' AND market_code in {market_check};")
    hh.append(f"SELECT * FROM dws.dws_file_market_segment_df WHERE market_code in {market_check};")
    yesterday = (datetime.date.today() - datetime.timedelta(days=1))
    zz.append(f"set hive.exec.compress.output=true;set "
              f"mapred.output.compression.codec=com.hadoop.compression.lzo.LzopCodec;INSERT OVERWRITE TABLE "
              f"ods.d_ods_file_market_segment_ful partition(dt='{yesterday}') SELECT "
              f"market_category,market_category_code,market_segment_desc ,market_segment,market_code_desc,market_code "
              f"from ods.d_ods_file_market_segment_ful WHERE dt='{dt}';INSERT INTO TABLE "
              f"ods.d_ods_file_market_segment_ful partition(dt='{yesterday}') values {sql1};")

    for i in zz:
        print(i)
    select_list=[]
    for i in hh:
        re = hive_sql(i)
        select_list.append(re)
    print(select_list)
