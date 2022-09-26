"""
author:风起于青萍之末，浪成于微澜之间
project:learn_python
date:2022/8/30
"""
# coding=utf8


import os
import re


def all_file(path):
    for i in os.listdir(path):
        i = os.path.join(path, i)
        if os.path.isdir(i):
            # print(f"{i}是文件夹")
            all_file(i)
        elif os.path.isfile(i):
            # print(f"{i}是文件")
            if i.endswith('txt'):
                j = re.sub(r'[a-z_]+(tdc_dc[a-z_]+?)(_?\d+)(\.txt)', r'\1\3', i)
                os.rename(i, j)
                print(f"{i}-->{j}")
        else:
            print("error")


def traversal_files(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            print(f'file is {os.path.join(root, name)}')
        for name in dirs:
            print(f'dir is {os.path.join(root, name)}')


def tra_files(path):
    for item in os.scandir(path):
        if item.is_dir():
            print(f'Dir :{item.path}')
            tra_files(item.path)
        elif item.is_file():
            print(item.path)


if __name__ == '__main__':
    file_path = r'D:/工作/其他/数据核对-20220830/'
    tra_files(file_path)
