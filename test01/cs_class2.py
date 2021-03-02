from test01 import cs_class

if __name__ == '__main__':

    b = cs_class.cs('ha')

    b.cs1()
    b.name = 'hehe'

    b.cs1()


def mysql_check(name):
    sql='select * from test.test1 where name_id=%s'%(name)
    print(sql)

mysql_check(12)















