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
                print(f'开始处理文件{ff}')
                read_file(ff)
                deal_sftp(ff)


def read_file(x):
    data = ''
    with open(x) as f1:
        lines = f1.readlines()
        for line in lines:
            if 'zip' in line and 'csv' in line and 'gpg' not in line and '_sales_$YYYY' not in line:
                csv_file = re.search(r'[a-zA-Z$_{}]*\.csv', line)
                zip_file = re.search(r'([a-zA-Z$_{}]*)\.zip', line)
                # print(zip_file.group())
                st = re.search(r'zip.*', line)

                print(
                    f'zip这一行替换{st.group()}为 rm -rf {zip_file.group()}.gpg && gpg --recipient tdc2crms  --always-trust --output {zip_file.group()}.gpg --encrypt {csv_file.group()}')
                line = re.sub(r'zip.*',
                              f'rm -rf {zip_file.group()}.gpg && gpg --recipient tdc2crms  --always-trust --output {zip_file.group()}.gpg --encrypt {csv_file.group()}',
                              line)
            elif 'ftp_crms.sh' in line and 'gpg' not in line and '_sales_$YYYY' not in line:
                zip_file = re.search(r'([a-zA-Z$_{}]*)\.zip', line)
                m1 = zip_file[0]
                m2 = zip_file[1]
                print(f'ftp_crms.sh 这一行替换{m1} 为 {m2}')
                line = line.replace(m1, f'{m2}.csv.gpg')

            elif 'split' in line and 'gpg' not in line and '_sales_$YYYY' not in line:
                zip_file = re.search(r'([a-zA-Z$_{}]*)\.zip', line)
                m1 = zip_file[0]
                m2 = zip_file[1]
                print(f'split 这一行替换{m1} 为 {m2}')
                line = line.replace(m1, f'{m2}.csv.gpg')

            data += line
        # print(data)
    with open(x, 'r+') as f2:
        f2.writelines(data)


def deal_sftp(x):
    with open(x) as f1:
        lines = f1.readlines()
        line = ''.join(lines)
        if ftp_str := re.search(
                "ftp\.upload[ \n]*conf: crms[ \n]*([a-zA-Z$_:/ ]*\.zip)",
                line,
                re.S,
        ):
            print(f'准备替换{x}中使用ftp节点给crms推数据的代码')
            z = re.sub('zip', 'csv.gpg', ftp_str[1])
            m1 = line.replace(ftp_str[1], z)
            with open(x, 'w') as f2:
                f2.writelines(m1)


if __name__ == '__main__':
    path = r'D:\dc-data-etl\etl_task\src\crms\profile\name_address'
    tra_files(path)
