import re
import subprocess

import pandas as pd
import time


def run_shell(cmd):
    sub = subprocess.Popen(""" %s """ % cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='.', shell=True)
    outs = []
    while sub.poll() is None:
        lines = sub.stdout.readlines()
        lines = [line.decode('utf-8', 'ignore') for line in lines]
        outs = outs + lines
        time.sleep(1)
    return sub.returncode, ''.join(outs)


def extract_partitions(table):
    cmd = """hive -e 'show partitions %s'""" % table
    (status, output) = run_shell(cmd)
    if status != 0:
        print('提取%s表分区失败' % table)
        return None
    r = re.findall('(\w+=[^\s]+)', output)
    r = list(map(lambda y: y.split('=')[1], r))
    if len(r) == 0:
        print(f"获取{table}分区失败")
        exit(1)
    return r


x = extract_partitions('ods.d_ods_file_market_segment_ful')
print(max(x))
