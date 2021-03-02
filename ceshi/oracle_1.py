
import cx_Oracle

with open('D:/工作/python/ceshi.txt','r',encoding='utf-8') as f :
    lines=f.readlines()
    for line in lines:
        lin=line.split()
        sql=('SELECT  {0[1]} FROM {0[0]} WHERE {0[1]} IS NOT NULL GROUP BY  {0[1]} ORDER BY {0[1]} '.format(lin))
        #print(sql)

        conn = cx_Oracle.connect('c##scott/scott@localhost/orcl')

        # 创建cursor
        cr = conn.cursor()
        # sql语句
        try:
            cr = cr.execute(sql)  # 执行sql语句

            # 一次返回所有的结果集
            results = cr.fetchall()
        except:  #查询错误的记录错误日志
            with open('D:/工作/python/err.log', 'a', encoding='utf-8') as f2:
                err='{0[0]}|{0[1]}'.format(lin) + '|查询异常！'
                print(err)
                f2.write(err+'\n')

        finally:

            with open('D:/工作/python/ceshi1.txt', 'a', encoding='utf-8') as f1:
                if results:
                    for re in results:
                        res=('{0[0]}|{0[1]}|{1[0]}'.format(lin,re))
                        print(res)
                        f1.write(res + '\n')
                else:
                    res=('{0[0]}|{0[1]} '.format(lin))
                    #print(res)
                    f1.write(res+'\n')
            cr.close()
            conn.close()
