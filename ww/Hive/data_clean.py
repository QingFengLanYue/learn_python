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
    print("exclude is %s" %exclude)
    g = dfs.groupby('hotel')
    # print(list(g))

    clean_df = pd.DataFrame(columns=['hotel', 'dt'])
    for (k, df) in g.__iter__():
        df.sort_values(by='dt', ascending=True, inplace=True)
        df = df.iloc[:-n, :]
        # if fl:
        #     df = df[eval(fl)]
        clean_df = clean_df.append(df.loc[:, ['dt', 'hotel']])
    clean_df.sort_values(by=['dt', 'hotel'], ascending=True, inplace=True)
    temp_partitions = clean_df.values.tolist()
    print(temp_partitions)
    temp_partitions = [x for x in temp_partitions if x not in exclude]
    return list(
        map(lambda x: """ALTER TABLE %s DROP IF EXISTS PARTITION (dt='%s', hotel='%s');""" % (table, x[0], x[1]),
            temp_partitions))



table_strategy = {'odc.t_fdm_pms_market_stat_daily_ful': ['keep_last_n_by_dt_hotel', {'fl': "~df['dt'].str.endswith('-01')", 'n': 2}]}
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
        partitions =[['2021-09-01', 'CNJJN001'], ['2021-09-01', 'CNSZV002'], ['2021-09-01', 'CWH'],['2021-09-03', 'CNJJN001'],
                       ['2021-09-01', 'CWSW'], ['2021-09-01', 'ESL'], ['2021-09-01', 'FIJ'], ['2021-09-01', 'GSH'],
                       ['2021-09-01', 'HBKC'], ['2021-09-01', 'HJB'], ['2021-09-01', 'ISL'], ['2021-09-01', 'KHHK'],
                       ['2021-09-01', 'KHPU'], ['2021-09-01', 'KSL'], ['2021-09-01', 'MAC'], ['2021-09-01', 'RRR'],
                       ['2021-09-01', 'RSR'], ['2021-09-01', 'SBHI'], ['2021-09-01', 'SEN'], ['2021-09-01', 'SHAR'],
                       ['2021-09-01', 'SHAS'], ['2021-09-01', 'SHHZ'], ['2021-09-01', 'SLAD'], ['2021-09-01', 'SLB'],
                       ['2021-09-01', 'SLBK'], ['2021-09-01', 'SLBO'], ['2021-09-01', 'SLBT'], ['2021-09-01', 'SLCB'],
                       ['2021-09-01', 'SLCC'], ['2021-09-01', 'SLCM'], ['2021-09-01', 'SLCZ'], ['2021-09-01', 'SLDA'],
                       ['2021-09-01', 'SLDB'], ['2021-09-01', 'SLDQ'], ['2021-09-01', 'SLFM'], ['2021-09-01', 'SLFT'],
                       ['2021-09-01', 'SLFZ'], ['2021-09-01', 'SLGL'], ['2021-09-01', 'SLH'], ['2021-09-01', 'SLLS'],
                       ['2021-09-01', 'SLUB'], ['2021-09-01', 'TSHY'], ['2021-09-02', 'CWH'],
                       ['2021-10-06', 'CNSZV002'], ['2021-10-06', 'CWH'], ['2021-10-06', 'CWSW'], ['2021-10-06', 'ESL'],
                       ['2021-10-06', 'FIJ'], ['2021-10-06', 'GSH'], ['2021-10-06', 'HBKC'], ['2021-10-06', 'HJB'],
                       ['2021-10-06', 'ISL'], ['2021-10-06', 'KHHK'], ['2021-10-06', 'KHPU'], ['2021-10-06', 'KSL'],
                       ['2021-10-06', 'MAC'], ['2021-10-06', 'RRR'], ['2021-10-06', 'RSR'], ['2021-10-06', 'SBHI'],
                       ['2021-10-06', 'SEN'], ['2021-10-06', 'SHAR'], ['2021-10-06', 'SHAS'], ['2021-10-06', 'SHHZ'],
                       ['2021-10-06', 'SLAD'], ['2021-10-06', 'SLB'], ['2021-10-06', 'SLBK'], ['2021-10-06', 'SLBO'],
                       ['2021-10-06', 'SLBT'], ['2021-10-06', 'SLCB'], ['2021-10-06', 'SLCC'], ['2021-10-06', 'SLCM'],
                       ['2021-10-06', 'SLCZ'], ['2021-10-06', 'SLDA'], ['2021-10-06', 'SLDB'], ['2021-10-06', 'SLDQ'],
                       ['2021-10-06', 'SLFM'], ['2021-10-06', 'SLFT'], ['2021-10-06', 'SLFZ'], ['2021-10-06', 'SLGL'],
                       ['2021-10-06', 'SLH'], ['2021-10-06', 'SLHF'], ['2021-10-06', 'SLHH'], ['2021-10-06', 'SLHI'],
                       ['2021-10-06', 'SLHN'], ['2021-10-06', 'SLIB'], ['2021-10-06', 'SLJ'], ['2021-10-06', 'SLJI'],
                       ['2021-10-06', 'SLJN'], ['2021-10-06', 'SLKL'], ['2021-10-06', 'SLLS'], ['2021-10-06', 'SLM'],
                       ['2021-10-06', 'SLMC'], ['2021-10-06', 'SLMZ'], ['2021-10-06', 'SLNB'], ['2021-10-06', 'SLNC'],
                       ['2021-10-06', 'SLND'], ['2021-10-06', 'SLNJ'], ['2021-10-06', 'SLP'], ['2021-10-06', 'SLPG'],
                       ['2021-10-06', 'SLPR'], ['2021-10-06', 'SLPU'], ['2021-10-06', 'SLQ'], ['2021-10-06', 'SLQF'],
                       ['2021-10-06', 'SLQH'], ['2021-10-06', 'SLS'], ['2021-10-06', 'SLSH'], ['2021-10-06', 'SLSN'],
                       ['2021-10-06', 'SLSZ'], ['2021-10-06', 'SLTJ'], ['2021-10-06', 'SLTN'], ['2021-10-06', 'SLTO'],
                       ['2021-10-06', 'SLTR'], ['2021-10-06', 'SLTS'], ['2021-10-06', 'SLTY'], ['2021-10-06', 'SLUB'],
                       ['2021-10-06', 'SLV'], ['2021-10-06', 'SLWU'], ['2021-10-06', 'SLWZ'], ['2021-10-06', 'SLXM'],
                       ['2021-10-06', 'SLXN'], ['2021-10-06', 'SLYW'], ['2021-10-06', 'SLYZ'], ['2021-10-06', 'SLZ'],
                       ['2021-10-06', 'SUR'], ['2021-10-06', 'TAH'], ['2021-10-06', 'THAD'], ['2021-10-06', 'THHK'],
                       ['2021-10-06', 'THKL'], ['2021-10-06', 'THM'], ['2021-10-06', 'THMD'], ['2021-10-06', 'THOG'],
                       ['2021-10-06', 'THPH'], ['2021-10-06', 'THS'], ['2021-10-06', 'TPE'], ['2021-10-06', 'TSHY']]
        hdfs_partitions = [['2021-09-01', 'CNJJN001'], ['2021-09-01', 'CNSZV002'], ['2021-09-01', 'CWH'],['2021-09-03', 'CNJJN001'],
                            ['2021-09-01', 'CWSW'], ['2021-09-01', 'ESL'], ['2021-09-01', 'FIJ'], ['2021-09-01', 'GSH'],
                            ['2021-09-01', 'HBKC'], ['2021-09-01', 'HJB'], ['2021-09-01', 'ISL'],
                            ['2021-09-01', 'KHHK'], ['2021-09-01', 'KHPU'], ['2021-09-01', 'KSL'],
                            ['2021-09-01', 'MAC'], ['2021-09-01', 'RRR'], ['2021-09-01', 'RSR'], ['2021-09-01', 'SBHI'],
                            ['2021-09-01', 'SEN'], ['2021-09-01', 'SHAR'], ['2021-09-01', 'SHAS'],
                            ['2021-09-01', 'SHHZ'], ['2021-09-01', 'SLAD'], ['2021-09-01', 'SLB'],
                            ['2021-09-01', 'SLBK'], ['2021-09-01', 'SLBO'], ['2021-09-01', 'SLBT'],
                            ['2021-09-01', 'SLCB'], ['2021-09-01', 'SLCC'], ['2021-09-01', 'SLCM'],
                            ['2021-09-01', 'SLCZ'], ['2021-09-01', 'SLDA'], ['2021-09-01', 'SLDB'],
                            ['2021-09-01', 'SLDQ'], ['2021-09-01', 'SLFM'], ['2021-09-01', 'SLFT'],
                            ['2021-09-01', 'SLFZ'], ['2021-09-01', 'SLGL'], ['2021-09-01', 'SLH'],
                            ['2021-09-01', 'SLLS'], ['2021-09-01', 'SLUB'], ['2021-09-01', 'TSHY'],
                            ['2021-09-02', 'CWH'], ['2021-10-06', 'CNSZV002'], ['2021-10-06', 'CWH'],
                            ['2021-10-06', 'CWSW'], ['2021-10-06', 'ESL'], ['2021-10-06', 'FIJ'], ['2021-10-06', 'GSH'],
                            ['2021-10-06', 'HBKC'], ['2021-10-06', 'HJB'], ['2021-10-06', 'ISL'],
                            ['2021-10-06', 'KHHK'], ['2021-10-06', 'KHPU'], ['2021-10-06', 'KSL'],
                            ['2021-10-06', 'MAC'], ['2021-10-06', 'RRR'], ['2021-10-06', 'RSR'], ['2021-10-06', 'SBHI'],
                            ['2021-10-06', 'SEN'], ['2021-10-06', 'SHAR'], ['2021-10-06', 'SHAS'],
                            ['2021-10-06', 'SHHZ'], ['2021-10-06', 'SLAD'], ['2021-10-06', 'SLB'],
                            ['2021-10-06', 'SLBK'], ['2021-10-06', 'SLBO'], ['2021-10-06', 'SLBT'],
                            ['2021-10-06', 'SLCB'], ['2021-10-06', 'SLCC'], ['2021-10-06', 'SLCM'],
                            ['2021-10-06', 'SLCZ'], ['2021-10-06', 'SLDA'], ['2021-10-06', 'SLDB'],
                            ['2021-10-06', 'SLDQ'], ['2021-10-06', 'SLFM'], ['2021-10-06', 'SLFT'],
                            ['2021-10-06', 'SLFZ'], ['2021-10-06', 'SLGL'], ['2021-10-06', 'SLH'],
                            ['2021-10-06', 'SLHF'], ['2021-10-06', 'SLHH'], ['2021-10-06', 'SLHI'],
                            ['2021-10-06', 'SLHN'], ['2021-10-06', 'SLIB'], ['2021-10-06', 'SLJ'],
                            ['2021-10-06', 'SLJI'], ['2021-10-06', 'SLJN'], ['2021-10-06', 'SLKL'],
                            ['2021-10-06', 'SLLS'], ['2021-10-06', 'SLM'], ['2021-10-06', 'SLMC'],
                            ['2021-10-06', 'SLMZ'], ['2021-10-06', 'SLNB'], ['2021-10-06', 'SLNC'],
                            ['2021-10-06', 'SLND'], ['2021-10-06', 'SLNJ'], ['2021-10-06', 'SLP'],
                            ['2021-10-06', 'SLPG'], ['2021-10-06', 'SLPR'], ['2021-10-06', 'SLPU'],
                            ['2021-10-06', 'SLQ'], ['2021-10-06', 'SLQF'], ['2021-10-06', 'SLQH'],
                            ['2021-10-06', 'SLS'], ['2021-10-06', 'SLSH'], ['2021-10-06', 'SLSN'],
                            ['2021-10-06', 'SLSZ'], ['2021-10-06', 'SLTJ'], ['2021-10-06', 'SLTN'],
                            ['2021-10-06', 'SLTO'], ['2021-10-06', 'SLTR'], ['2021-10-06', 'SLTS'],
                            ['2021-10-06', 'SLTY'], ['2021-10-06', 'SLUB'], ['2021-10-06', 'SLV'],
                            ['2021-10-06', 'SLWU'], ['2021-10-06', 'SLWZ'], ['2021-10-06', 'SLXM'],
                            ['2021-10-06', 'SLXN'], ['2021-10-06', 'SLYW'], ['2021-10-06', 'SLYZ'],
                            ['2021-10-06', 'SLZ'], ['2021-10-06', 'SUR'], ['2021-10-06', 'TAH'], ['2021-10-06', 'THAD'],
                            ['2021-10-06', 'THHK'], ['2021-10-06', 'THKL'], ['2021-10-06', 'THM'],
                            ['2021-10-06', 'THMD'], ['2021-10-06', 'THOG'], ['2021-10-06', 'THPH'],
                            ['2021-10-06', 'THS'], ['2021-10-06', 'TPE'], ['2021-10-06', 'TSHY']]
        partitions_df = pd.DataFrame(partitions, columns=partition_fields)
        hdfs_partitions_df = pd.DataFrame(hdfs_partitions, columns=partition_fields)
        hdfs_partitions_df = hdfs_partitions_df.drop_duplicates(subset=partition_fields, keep='first')
        merge_df = pd.merge(partitions_df, hdfs_partitions_df, on=partition_fields)

        print("partitions_df is %s"%partitions_df)
        print("hdfs_partitions_df is %s" % hdfs_partitions_df)
        print("merge_df is %s" % merge_df)


        f = eval(v[0])
        print(v[1])
        clean_ddl = f(merge_df, k, **v[1])
        print(clean_ddl)
        # with open(file_path, 'a') as hive_w:
        #     hive_w.writelines('\n-- ------------------------------------')
        #     hive_w.writelines('\n' + '\n'.join(clean_ddl))


