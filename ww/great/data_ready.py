"""
author:cai
project:learn_python
date:2021/12/29
"""
# coding=utf8
import re
import sqlite3
import pandas as pd
import ruamel_yaml
from conda.common.serialize import yaml

con = sqlite3.connect("test.db")
cur = con.cursor()


def txt_deal(name):
    with open(name) as f:
        isql = ''
        x = f.readlines()
        for y in x:
            y = re.sub("'", "\'", y)
            # y = re.sub("\(", '\(', y)
            # y = re.sub('\)', '\)', y)
            y = y.split('|?~!^')
            y = '","'.join(y)
            y = re.sub('\n', '', y)

            isql = isql + '("' + y + '"),'
        isql = re.sub(',$', ';\n', isql)
    return isql


def insert_sql(d):
    insql = ''
    for x in d.keys():
        sql = d.get(x)
        sql = f'insert into {x}(' + ','.join(sql) + ') values'
        values = txt_deal('data/' + x + '.txt')
        sql = sql + values
        insql = insql + sql
        # print(insql)
        cur.execute(sql)
        cur.execute('commit')


def load_yaml(path):
    file_path = path
    f = open(file_path, "r")
    return yaml.load(f, Loader=ruamel_yaml.Loader)


def create_table():
    a = load_yaml('conf.yaml')
    # b = pd.DataFrame(a)
    # print(b)
    for i in a.keys():
        t = pd.DataFrame(a.get(i))
        t1 = [f'{k} {v}' for k, v in t[['column', 'type']].values.tolist()]
        fields = ',\n'.join(t1)
        s = f"""create table if not exists {i} ({fields});\n"""

        cur.execute(s)


def table_list():
    a = load_yaml('conf.yaml')
    # b = pd.DataFrame(a)
    # print(b)
    s = {}
    for i in a.keys():
        t = pd.DataFrame(a.get(i))
        t1 = [f'{k}' for k in t['column'].values.tolist()]
        s[i] = t1
    return s


if __name__ == '__main__':
    cur.execute("drop table if exists main;")
    cur.execute("drop table if exists detail")
    create_table()
    column_list = table_list()
    insert_sql(column_list)
    cur.close()
