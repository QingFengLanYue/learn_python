import sys
import os

email_template = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>Title</title>
    <style type='text/css'>
        table {
            border-collapse:collapse;
        }
        #table-7 thead th {
            background-color: rgb(81, 130, 187);
            color: #fff;
            border-bottom-width: 0;
        }

        #table-7 td {
            color: #000;
        }
        #table-7 tr, #table-7 th {
            border: 1px solid rgb(81, 130, 187);
        }

        #table-7 td, #table-7 th {
            padding: 5px 10px;
            font-size: 14.67px;
            font-family: Calibri;
            font-weight: bold;
            text-align: center;
        }
        #table-7 td, #table-7 th {
            padding: 5px 10px;
            font-size: 14.67px;
            font-family: Calibri;
            font-weight: bold;
            text-align: center;
        }

        body,pre {
            font-size: 14.67px; 
            font-family: Calibri; 
        }
    </style>
</head>
<body>
<pre>
Dear all,

Greetings from Shangri-la TDC DataCenter team! 
We are writing to seek your assistance regarding missing data from the cloud POS to the TDC DataCenter.

</pre>



<table id='table-7'>
    message
</table>


<pre>
Thank you and best regards
TDC DataCenter Team.
</pre>
</body>
</html>



"""

table_list = [
    'ods_infrasys_cloud_check_di',
    'ods_infrasys_cloud_checkitem_di',
    'ods_infrasys_cloud_checkpayment_di',
    'ods_infrasys_cloud_departmentsales_di',
    'ods_infrasys_cloud_paymentsummary_di',
    'ods_infrasys_cloud_taxsummary_di',
    'ods_infrasys_cloud_users_di'
]
exclude_list = [
    # {'hotel': 'TEST_01', 'begin_date': '2022-08-06', 'end_date': '2022-08-07'}
]

sql_dict = {}
check_sql = """
SELECT NVL(hotel,'ALL_HOTEL') hotel
      ,min_date stat_start_date
      ,miss_date
FROM (SELECT hotel, natural_date miss_date,min_date,MAX(fdate) fdate
        FROM (SELECT infrasys.hotel
                    ,cal.natural_date
                    ,CASE
                        WHEN infrasys.fdate = cal.natural_date THEN
                        cal.natural_date
                    END fdate
                    ,min_date
            FROM (SELECT natural_date, 1 flag
                    FROM dim_pub_calendar_date
                    WHERE natural_date > date_sub(TO_DATE('{bizdate}', 'YYYYMMDD'), {days})
                    AND dt_num <= '{bizdate}') cal
            LEFT JOIN (SELECT  hotel
                              ,CASE WHEN fdate NOT like '%-%' THEN TO_CHAR(TO_DATE(fdate,'YYYYMMDD'),'YYYY-MM-DD') ELSE fdate end fdate
                              ,min(CASE WHEN fdate NOT like '%-%' THEN TO_CHAR(TO_DATE(fdate,'YYYYMMDD'),'YYYY-MM-DD') ELSE fdate end) over(partition by hotel) min_date
                              ,1 flag
                        FROM {table}
                        WHERE dt > TO_CHAR(date_sub(TO_DATE('{bizdate}', 'YYYYMMDD'), {days}),'YYYYMMDD')
                        GROUP BY hotel, fdate
                        ) infrasys
            ON cal.flag = infrasys.flag) infrasys
        GROUP BY hotel, natural_date ,min_date)
WHERE fdate IS NULL AND miss_date > min_date {exclude_sql}
"""

exclude_sql = ''
if exclude_list:
    for exclude_code in exclude_list:
        exclude_sql += f""" \nAND (hotel <> '{exclude_code['hotel']}' OR miss_date NOT BETWEEN '{exclude_code['begin_date']}' AND '{exclude_code['end_date']}')"""

for table in table_list:
    sql_dict[table] = check_sql.format(table=table, bizdate=bizdate, exclude_sql=exclude_sql, days=365)

check_result = {}
for key, value in sql_dict.items():
    # print(key, value)
    with o.execute_sql(value).open_reader(tunnel=True) as reader_resv:
        # pd_df 类型为 pandas DataFrame
        check_result[key] = reader_resv.to_pandas()

all_empty = all(df.empty for df in check_result.values())

if not all_empty:
    result_list = ""

    for table, value in check_result.items():
        result_template = f'''
            <tbody>
            <p>
                {{% if not check_result['{table}'].empty %}}The {table} table data is missing as below:
                {{{{check_result['{table}'].sort_values(['hotel', 'miss_date']).to_html(index=False)}}}}{{% endif %}}
            </p>
        </tbody>
        '''
        result_list += result_template

    email_template = email_template.replace('message', result_list)

    subject = "[Action Required] infrasys cloud check mail"

    mail.send(alert_email_from, alert_email_to, subject, content)
else:
    print("数据正常，没有需要报警的内容")
