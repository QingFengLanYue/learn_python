"""
author:cai
project:learn_python
date:2021/11/25
"""
# coding=utf8

import pandas as pd
import pymysql


def decorate(func):
    def except_deal(sql):
        try:
            return func(sql)
        except pymysql.err.ProgrammingError as e:
            print('Sql 语句报错', e)
            # 捕获由于sql语句错误抛出的异常
            # 捕获后的操作
        except pymysql.err.IntegrityError as e:
            print('主键冲突,请核对后重新输入\n', e)

    return except_deal


# mysql 连接
def con_my():
    host = 'localhost'
    port = 3306
    user = 'root'
    password = 'root'
    db = 'test'
    conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8')
    cur = conn.cursor()
    return conn, cur


@decorate
def check_exists(sql):
    conn, cur = con_my()
    # print(sql)
    cur.execute(sql)
    col_names = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    rows = pd.DataFrame(rows, columns=col_names)
    return rows


def change_str(series):
    l = []
    m = {}
    type1 = 'keep_last_n' if series['partition_type'] == 1 else 'keep_last_n_by_dt_hotel'
    save_01_type = "~df['dt'].str.endswith('-01')" if series['save_dd_01_yn'] == 'Y' else None

    m['fl'] = save_01_type
    m['n'] = series['save_partition_num']
    l.append(type1)
    l.append(m)
    return l


if __name__ == '__main__':
    sql = "select * from test.hive_data_life_cycle_management"
    s = check_exists(sql)
    s["save_01_type"] = s.apply(change_str, axis=1)

    # s["save_01_type"] = s.apply(lambda x: change_str(s), axis=1)

    print(dict(zip(s['table_name'], s["save_01_type"])))

# table_strategy ="""
# {'dws.dws_pms_transaction_stat_df': ['keep_last_n_by_dt_hotel', {'fl': "~df['dt'].str.endswith('-01')", 'n': 7}] }
# """
