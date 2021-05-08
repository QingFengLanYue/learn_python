'''
author:cai
project:learn_python
date:2021/5/8
'''

from test01.sql_mysql import *
import pandas as pd

scheam = 'test'
table_name = 'stay_record_test'

sql1 = '''
      select COLUMN_NAME from information_schema.columns 
        where table_schema = '%s'  #表所在数据库 
        and table_name = '%s'
        ORDER BY ORDINAL_POSITION
      ''' %(scheam,table_name)
#print(sql1)
co = mysql_select(sql1)
df_tab1 = pd.DataFrame(co,columns=['column'])
columns = df_tab1['column'].tolist()

sql2 = 'select * from stay_record_test'

re = mysql_select(sql2)

df_re = pd.DataFrame(re,columns=columns)

df1=df_re.loc[df_re['conf_no'].isin(['10712067225','10368521142'])]

print(df1[['id','conf_no','detail']])
