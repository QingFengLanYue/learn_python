'''
author:cai
project:learn_python
date:2021/5/8
'''
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
        connection = pymysql.connect(**config)
        #print("connect mysql ok")
        return connection
    except pymysql.Error as err:
        print("Connect mysql with config=", config, " error=", err)
        return False

def cur_mysql_conn():
    conn = connect()
    cur = conn.cursor()
    return conn,cur


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
        except Exception:  # 方法一：捕获所有异常
            # 如果发生异常，则回滚
            print("发生异常", Exception)
    return except_deal

@decorate
def func_1(args):
    print(args)

@decorate
def mysql_insert(sql):
    # conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='test', charset='utf8')
    # cur = conn.cursor()
    conn,cur = cur_mysql_conn()
    cur.execute(sql)
    cur.execute('commit')
    cur.close()
    conn.close()
    print(sql)


@decorate
def mysql_select(sql):
    conn,cur = cur_mysql_conn()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


@decorate
def mysql_delete(sql):
    conn,cur = cur_mysql_conn()
    cur.execute(sql)
    cur.execute('commit')
    cur.close()
    conn.close()
    print(sql)


@decorate
def mysql_update(sql):
    conn,cur = cur_mysql_conn()
    cur.execute(sql)
    cur.execute('commit')
    cur.close()
    conn.close()
    print(sql)
