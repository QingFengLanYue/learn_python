"""
author:cai
project:learn_python
date:2021/11/19
"""
# coding=utf8


# coding=utf8
import pandas as pd
import re
import os
import subprocess
import time

import shutil

LF = '\n'
BK = ' '


def run_shell(cmd):
    sub = subprocess.Popen(""" %s """ % cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='.', shell=True)
    outs = []
    while sub.poll() is None:
        lines = sub.stdout.readlines()
        lines = [line.decode('utf-8', 'ignore') for line in lines]
        outs = outs + lines
        time.sleep(1)
    return sub.returncode, ''.join(outs)


# 保留最后一个分区
def keep_last_n(df, table, n=1, fl=None):
    df.sort_values('dt', ascending=True, inplace=True)
    df = df.iloc[:-n, [0]]
    if fl:
        df = df[eval(fl)]
    temp_partitions = df.iloc[:, 0].values.tolist()
    return list(map(lambda x: """ALTER TABLE %s DROP IF EXISTS PARTITION (dt='%s');""" % (table, x), temp_partitions))


def cpm_keep_last_n(dfs, table, n=1, fl=None):
    dfs.sort_values(by=list(dfs.columns), ascending=True, inplace=True)
    g = dfs.groupby(dfs.columns[0])
    clean_df = pd.DataFrame(columns=list(dfs.columns))
    for (k, df) in g.__iter__():
        df.sort_values(by=list(dfs.columns)[1:], ascending=True, inplace=True)
        df = df.iloc[:-n, :]
        if fl:
            df = df[eval(fl)]
        clean_df = clean_df.append(df.loc[:, :])
    clean_df.sort_values(by=list(dfs.columns), ascending=True, inplace=True)
    temp_partitions = clean_df.values.tolist()
    return list(map(lambda x: """ALTER TABLE %s DROP IF EXISTS PARTITION (%s);""" % (table
                                                                                     , ','.join(
        ["%s='%s'" % (y[0], y[1]) for y in zip(df.columns, x)])
                                                                                     ), temp_partitions))


def keep_last_n_by_dt_hotel(dfs, table, n=1, fl=None):
    dfs.sort_values(by=['hotel', 'dt'], ascending=True, inplace=True)
    history = dfs.copy()
    history['month'] = history['dt'].apply(lambda x: f"{x.split('-')[0]}-{x.split('-')[1]}")
    history.drop_duplicates(subset=['hotel', 'month'], keep='first', inplace=True)
    exclude = history[['dt', 'hotel']].values.tolist()
    g = dfs.groupby('hotel')

    clean_df = pd.DataFrame(columns=['hotel', 'dt'])
    for (k, df) in g.__iter__():
        df.sort_values(by='dt', ascending=True, inplace=True)
        df = df.iloc[:-n, :]
        # if fl:
        #     df = df[eval(fl)]
        clean_df = clean_df.append(df.loc[:, ['dt', 'hotel']])
    clean_df.sort_values(by=['dt', 'hotel'], ascending=True, inplace=True)
    temp_partitions = clean_df.values.tolist()
    temp_partitions = [x for x in temp_partitions if x not in exclude]
    return list(
        map(lambda x: """ALTER TABLE %s DROP IF EXISTS PARTITION (dt='%s', hotel='%s');""" % (table, x[0], x[1]),
            temp_partitions))



table_strategy = {'odc.t_fdm_pms_market_stat_daily_ful': ['keep_last_n_by_dt_hotel', {'fl': "~df['dt'].str.endswith('-01')", 'n': 3}]}
def fetch_create_table(table):
    cmd = """hive -e 'show create table %s'""" % table
    (status, output) = run_shell(cmd)
    if status != 0:
        print('提取%s表结构失败' % table)
        return None
    return output.replace(LF, BK)


def extract_partition_field(ddl):
    r = re.findall(r"PARTITIONED BY \([^)]*\)", ddl)
    if len(r) > 0:
        ps = re.findall(r"`([^`]*)`", r[0])
        return ps
    return []


def extract_partitions(table):
    cmd = """hive -e 'show partitions %s'""" % table
    (status, output) = run_shell(cmd)
    if status != 0:
        print('提取%s表分区失败' % table)
        return None
    r = re.findall('(\w+=[^\s]+)', output)
    r = map(lambda x: list(map(lambda y: y.split('=')[1], x.split('/'))), r)
    return list(r)


def extract_hdfs_partitions(table, ps):
    db = table.split('.')[0]
    table_name = table.split('.')[1]
    pt = '/'.join([f'{x}=*'for x in ps])
    cmd = f"""hdfs dfs -ls /user/hive/warehouse/{db}.db/{table_name}/{pt}"""
    print(cmd)
    (status, output) = run_shell(cmd)
    if status != 0:
        print('提取%s表hdfs分区失败' % table)
        return None
    pt = '/'.join([f'{x}=.*?' for x in ps]) + '/'
    print(pt)
    r = re.findall(pt, output)
    result = map(lambda x: list(map(lambda y: y.split('=')[1], x.strip('/').split('/'))), r)
    return list(result)


def clean_file(path):
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)


if __name__ == '__main__':
    # file_path = '/tmp/hive_clean.ddl'
    # clean_file(file_path)
    for k, v in table_strategy.items():
        print('正在处理: %s' % k)
        partition_fields = ['dt', 'hotel']
        partitions =[['2021-09-03', 'CWH'], ['2021-10-03', 'CWH'], ['2021-09-01', 'CWH'],['2021-10-16', 'CWH']
        ,['2021-10-04', 'CWH'], ['2021-10-05', 'CWH']
            ,['2021-09-05', 'CWH'],['2021-09-02', 'CWH'],['2021-10-06', 'CWH'], ['2021-10-01', 'CWH']]
        partitions=sorted(partitions)
        hdfs_partitions = [['2021-09-01', 'CWH'],['2021-09-02', 'CWH'], ['2021-10-01', 'CWH']
                            ,['2021-09-03', 'CWH'],['2021-10-03', 'CWH'], ['2021-10-04', 'CWH'],['2021-10-05', 'CWH'],['2021-10-16', 'CWH']]
        hdfs_partitions=sorted(hdfs_partitions)
        print(hdfs_partitions)
        partitions_df = pd.DataFrame(partitions, columns=partition_fields)
        hdfs_partitions_df = pd.DataFrame(hdfs_partitions, columns=partition_fields)
        hdfs_partitions_df = hdfs_partitions_df.drop_duplicates(subset=partition_fields, keep='first')
        merge_df = pd.merge(partitions_df, hdfs_partitions_df, on=partition_fields)

        # print("partitions_df is %s"%partitions_df)
        # print("hdfs_partitions_df is %s" % hdfs_partitions_df)
        # print("merge_df is %s" % merge_df)

        pd.set_option('display.max_rows', None)
        f = eval(v[0])
        print(v[1])
        clean_ddl = f(merge_df, k, **v[1])
        print(clean_ddl)
        # with open(file_path, 'a') as hive_w:
        #     hive_w.writelines('\n-- ------------------------------------')
        #     hive_w.writelines('\n' + '\n'.join(clean_ddl))


