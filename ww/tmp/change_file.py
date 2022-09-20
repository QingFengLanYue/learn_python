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
                os.rename(i,j)
                print(f"{i}-->{j}")
        else:
            print("error")


if __name__ == '__main__':
    file_path = r'D:/工作/其他/数据核对-20220830/'
    all_file(file_path)
