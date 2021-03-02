import functools
import logging
import pymysql
import pandas as pd
import re
import functools

# def foo():
#     print("is foo")
#
# def bar(func):
#     func()
#
# bar(foo)



def cur_conn():
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='test', charset='utf8')
    cur = conn.cursor()
    return conn,cur


def conn_mysql_insert(sql):
    # conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='test', charset='utf8')
    # cur = conn.cursor()
    conn,cur = cur_conn()
    cur.execute(sql)
    cur.execute('commit')
    cur.close()
    conn.close()

sql="insert into test.cs_01(id,name,detial) values('1','zhangsan','detial_list{(01,29),(03,67),(04,66)}');"

#conn_mysql_insert(sql)




#deal_except(conn_mysql_insert(sql))


# def exce_del():
#     pass
#
# def log(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         print('call %s():' % func.__name__)
#         print('args = {}'.format(*args))
#         return func(*args)
#
#     return wrapper
#
# @log
# def test(p):
#     print(test.__name__ + " param: " + p)
#
#
# test("I'm a param")
#
#
#
# def funA(fn):
#     print("C语言中文网")
#     fn() # 执行传入的fn参数
#     print("http://c.biancheng.net")
#     return "装饰器函数的返回值"
# @funA
# def funB():
#     print("学习 Python")
#
#
# def funA(fn):
#     # 定义一个嵌套函数
#     def say(arc):
#         print("Python教程:",arc)
#     return say
# @funA
# def funB(arc):
#     print("say")
# funB("http://c.biancheng.net/python")


# def deal_except(fuc):
#     def exp_deal(fuc):
#         try:
#             fuc
#         except pymysql.err.ProgrammingError as e:
#             print('Sql 语句报错',e)
#         # 捕获由于sql语句错误抛出的异常
#         # 捕获后的操作
#         except pymysql.err.IntegrityError as e:
#             print('主键冲突',e)
#     return exp_deal
#
# @deal_except
# def conn_mysql_insert(sql):
#     # conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='test', charset='utf8')
#     # cur = conn.cursor()
#     conn,cur = cur_conn()
#     cur.execute(sql)
#     cur.execute('commit')
#     cur.close()
#     conn.close()

#conn_mysql_insert("insert into test.cs_01(id,name,detial) values('1','zhangsan','detial_list{(01,29),(03,67),(04,66)}');")



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

@decorate
def func_1(args):
    print(args)

@decorate
def conn_mysql_insert(sql):
    # conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='test', charset='utf8')
    # cur = conn.cursor()
    conn,cur = cur_conn()
    cur.execute(sql)
    cur.execute('commit')
    cur.close()
    conn.close()
    print(sql)

conn_mysql_insert("insert into test.cs_01(id,name,detial) values('1','zhangsan','detial_list{(01,29),(03,67),(04,66)}');")



def zsq(f1):
    #@functools.wraps(f1)
    def excepF1(st):
        print('zsq test 1 ')
        f1(st)
        print('zsq test 2')
    return excepF1


@zsq
def cs(st):
    print("This is "+st)

cs2=cs('first cs')
print(cs.__name__)

# if __name__ == '__main__':
#     #conn_mysql_insert("insert into test.cs_01(id,name,detial) values('1','zhangsan','detial_list{(01,29),(03,67),(04,66)}');")
#     pass
#
#
#
#
#
# class Foo(object):
#     def __init__(self, func):
#         self._func = func
#
#     def __call__(self,*args):
#         print ("class decorator runing %s"% (args,))
#         self._func(*args)
#         print ('class decorator ending %s'% (args,))
#
# @Foo
# def bar(st1,st2):
#     print ('bar %s,%s' %(st1,st2))
#
# bar('hhhhh','eeeee')