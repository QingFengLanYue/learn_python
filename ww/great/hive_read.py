from impala.dbapi import connect
import pandas as pd


def hive_conn(hsql, num):
    conn = connect(host='10.0.0.0', port=10000, database='tmp', auth_mechanism='PLAIN')
    # print(cursor.description)  # prints the result set's schema
    res = pd.read_sql(hsql, conn, chunksize=num, parse_dates=['ccre_date', 'create_time'])
    return res


if __name__ == '__main__':
    sql = 'select * from tmp.greate limit 10'
    r = hive_conn(sql, num=20)
    for x in r:
        print(x)
