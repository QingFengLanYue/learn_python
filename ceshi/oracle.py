# encoding:utf-8
import cx_Oracle

# 连接oracle数据库
#conn = cx_Oracle.connect('system/oracle@localhost/orcl')
conn = cx_Oracle.connect('c##scott/scott@localhost/orcl')

# 创建cursor
cr = conn.cursor()
# sql语句

sql = "select * from  name"
#pr = {'a':'30'}
cr = cr.execute(sql)  # 执行sql语句

# 一次返回所有的结果集使用 fetchall
results = cr.fetchall()
for re in results:
    print(re)

# 一次返回一行 fetchone
while (1):
    re = cr.fetchone()
    if re == None:
        break
    print(re)

cr.close()
conn.close()
