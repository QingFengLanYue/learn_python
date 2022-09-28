"""
author:风起于青萍之末，浪成于微澜之间
project:learn_python
date:2022/9/27
"""
# coding=utf8
import os
import pymysql

config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'test',
    'charset': "utf8"
}


def connect():
    try:
        return pymysql.connect(**config)
    except pymysql.Error as err:
        print("Connect mysql with config=", config, " error=", err)
        return False


def cur_mysql_conn():
    conn = connect()
    cur = conn.cursor()
    return conn, cur


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
        except Exception as e:  # 方法一：捕获所有异常
            # 如果发生异常，则回滚
            print("发生异常", e)

    return except_deal


@decorate
def mysql_insert(sql):
    conn, cur = cur_mysql_conn()
    cur.execute("use test")
    cur.execute("SET NAMES utf8mb4")
    cur.execute("SET CHARACTER SET utf8mb4")
    cur.execute("SET character_set_connection = utf8mb4")
    cur.execute(sql)
    cur.execute('commit')
    cur.close()
    conn.close()


if __name__ == '__main__':
    sql_dir = r'D:\工作\DR3\20220926\great'
    # for x in os.scandir(sql_dir):
    #     mysql_insert(x.path)
    os.chdir(sql_dir)
    for x in os.scandir(os.curdir):
        print(x.path)
        with open(x.path, encoding='utf8') as f:
            insert_sql = f.read()
            mysql_insert(insert_sql)
