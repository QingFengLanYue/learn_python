import http.client
import socket
import time
import urllib

import pandas as pd
import psutil

import pymysql


conf = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'test'
}

hosts = socket.gethostname()

template = """
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
            font-size: 12px;
            font-family: Verdana;
            font-weight: bold;
        }
    </style>
</head>
<body>

<pre>
Dear All,
    丢失进程的任务列表如下:

</pre>



<table id='table-7'>

    <tbody>
        content
    </tbody>
</table>


<pre>
Thank you and best regards
</pre>
</body>
</html>
"""


def sql_select(sql):
    conn = pymysql.connect(**conf)
    cur = conn.cursor()
    try:
        print(sql)
        cur.execute(sql)
        col = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        rows = pd.DataFrame(list(rows), columns=col)
        rows = rows.set_index('pid')
        return rows
    except Exception as e:
        print("发生异常", e)
    finally:
        cur.close()
        conn.close()


def sql_update(sql):
    conn = pymysql.connect(**conf)
    cur = conn.cursor()
    try:
        print(sql)
        cur.execute(sql)
        n = cur.rowcount
        cur.execute('commit')
        return n
    except Exception as e:
        print("发生异常", e)
    finally:
        cur.close()
        conn.close()


def time_stamp():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def pid_check(run_task):
    for pid in run_task.index.values:
        try:
            psutil.Process(pid)
            run_task.loc[pid, 'flag'] = 1
        except Exception as e:
            print('except:', time_stamp(), e)
            run_task.loc[pid, 'flag'] = 0
    return run_task[run_task['flag'] == 0]


def send_alert(subject, content, names):
    params = urllib.parse.urlencode(
        {
            'title': subject.encode('utf-8') if subject else "",
            'content': content or "",
            'names': names.encode('utf-8') if names else "",
        }
    )

    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn = http.client.HTTPConnection(dc_schedule_server)
    conn.request("POST", "/alarm/sendMail", params, headers)
    response = conn.getresponse()
    conn.close()
    if response.status == 200:
        print("send alarm info succeed")
    else:
        print(f"send alarm mail fail, errorinfo: {response.reason}")
        exit(1)


def unlock_task(error_task):
    error_task = error_task.to_dict(orient='records')

    time.sleep(60)

    for i in error_task:
        run_log_id = i.get('id')
        task_id = i.get('task_id')
        pid = s[s['task_id'] == task_id].index.values.tolist()[0]
        print(f"{time_stamp()},任务{task_id}对应的进程{pid}没有找到")
        # 修改日志状态为失败
        sql1 = f"update run_log set run_status=3 where id = {run_log_id} and run_status = 1 and machine='{hosts}'"
        # 任务解锁
        sql2 = f"update task set is_locked=0 where id = {task_id} and machine='{hosts}'"

        n = sql_update(sql1)
        if n == 1:
            sql_update(sql2)
            err_proc.append(run_log_id)
        else:
            print(f"{time_stamp()},任务{task_id}已经自动执行完成")
    return err_proc


if __name__ == '__main__':

    run_task_sql = f"select * from run_log where run_status = 1 and machine='{hosts}'"

    dc_schedule_server = "lisi.com"
    sends = ['zhang.san']

    s = sql_select(run_task_sql)
    if s.empty:
        print(f"{time_stamp()},没有任务运行...")
        exit(0)

    err_task = pid_check(s)
    err_proc = []

    if err_task.empty:
        print(f"{time_stamp()},任务进程正常...")
    else:
        err_proc = unlock_task(err_task)
        email_content = s[s['id'].isin(err_proc)].reset_index().to_html()

        # print(template.replace('content', content))
        if err_proc:
            send_alert("任务进程监控报警", template.replace('content', email_content), ','.join(set(sends)))

