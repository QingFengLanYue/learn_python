"""
author:风起于青萍之末，浪成于微澜之间
project:learn_python
date:2023/1/17
"""
# coding=utf8
import os
import re

def tra_files(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for f in files:
            if f.endswith('yaml'):
                ff = os.path.join(root, f)
                read_file(ff)

def read_file(x):
    data=''
    with open(x) as f1:
        lines = f1.readlines()
        for line in lines:
            if 'zip' in line and 'csv' in line and 'gpg' not in line and '_sales_$YYYY$mm$dd' not in line:
                csv_file = re.search(r'[a-zA-Z$_]*\.csv', line)
                line = re.sub('zip.*',f'rm {csv_file.group()}.gpg && gpg --recipient tdc2crms  --always-trust --output {csv_file.group()}.gpg --encrypt {csv_file.group()}',line)
            elif 'ftp_crms.sh' in line and 'gpg' not in line and '_sales_$YYYY$mm$dd' not in line:
                zip_file = re.search(r'([a-zA-Z$_]*)\.zip', line)
                m1 = zip_file[0]
                m2 = zip_file[1]
                line = line.replace(m1,f'{m2}.csv.gpg')
            else:
                line = line
            data+=line
    with open(x,'r+') as f2:
        f2.writelines(data)




if __name__ == '__main__':
    path = r'D:\dc-data-etl\etl_task\src\crms\baseinfo'
    tra_files(path)