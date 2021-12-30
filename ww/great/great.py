"""
author:cai
project:learn_python
date:2021/12/29
"""
# coding=utf8

import sqlite3
import pandas as pd
from ww.great import data_ready

con = sqlite3.connect("test.db")
cur = con.cursor()
hh = con.cursor()
column_list = data_ready.table_list()

cur.execute("select * from detail")
m = cur.fetchmany(3)


def main_deal(x):
    main_sql = f"select * from main where defecttrack_mainid={x}"
    print(main_sql)
    hh.execute(main_sql)
    print(hh.fetchall())


while m:
    table_detail = pd.DataFrame(m, columns=column_list.get('detail'))
    mainid = table_detail['defecttrack_mainid']
    for x in mainid:
       main_deal(x)
    m = cur.fetchmany(3)
    print("下一批")
