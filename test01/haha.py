#
from __future__ import print_function

import os
import random
import pandas as pd

pool=[]
for i in range(48,58):
    pool.append(chr(i))

for i in range(65,91):
    pool.append(chr(i))

for i in range(97,123):
    pool.append(chr(i))

for index in range(0,4):
    x=random.randrange(0,62)
    print(pool[x],end=' ')

print('-----------------------------',end='\n')
import re

str_words='我下班了123AAa234aserERTFV，该吃个饭了'
str_num=re.compile(r'[0-9]')
str_al=re.compile(r'[a-zA-Z]')
str_ch=re.compile(r'[\u4E00-\u9FA5]')

num=str_num.findall(str_words)
st=str_al.findall(str_words)
ch=str_ch.findall(str_words)
print(num)
print(st)
print(ch)



import os  # Import the OS module

MESSAGE = 'The directory already exists.'
TESTDIR = 'D:/test/testdir'
try:
    home = os.path.expanduser("~")  # Set the variable home by expanding the user's set home directory
    print(home)
    print("Will create dir is :",TESTDIR)  # Print the location

    if not os.path.exists(os.path.join(TESTDIR)):  # os.path.join() for making a full path safely
        os.makedirs(os.path.join(TESTDIR))  # If not create the directory, inside their home directory
    else:
        print(MESSAGE)
except Exception as e:
    print(e)





# def main():
#     CheckDir = input("Enter the name of the directory to check : ")
#     print()
#
#     if os.path.exists(CheckDir):  # Checks if the dir exists
#         print("The directory exists")
#     else:
#         print("No directory found for " + CheckDir)  # Output if no directory
#         # print()
#         os.makedirs(CheckDir)  # Creates a new dir for the given name
#         print("Directory created for " + CheckDir)
#
#
# if __name__ == '__main__':
#     main()


import os
import stat  # index constants for os.stat()
import sys
import time

if sys.version_info >= (3, 0):
    raw_input = input

# file_name = raw_input("Enter a file name: ")  # pick a file you have
file_name = "D:/test/test1/test.txt"
count = 0
t_char = 0

try:
    with open(file_name) as f:
        count = (sum(1 for line in f))
        f.seek(0)
        t_char = (sum([len(line) for line in f]))
except FileNotFoundError as e:
    print(e)
    sys.exit(1)
# When open item is a directory (python2)
except IOError:
    pass
# When open item is a directory (python3)
except IsADirectoryError:
    pass

file_stats = os.stat(file_name)
# create a dictionary to hold file info
file_info = {
    'fname': file_name,
    'fsize': file_stats[stat.ST_SIZE],
    'f_lm': time.strftime("%d/%m/%Y %I:%M:%S %p",
                          time.localtime(file_stats[stat.ST_MTIME])),
    'f_la': time.strftime("%d/%m/%Y %I:%M:%S %p",
                          time.localtime(file_stats[stat.ST_ATIME])),
    'f_ct': time.strftime("%d/%m/%Y %I:%M:%S %p",
                          time.localtime(file_stats[stat.ST_CTIME])),
    'no_of_lines': count,
    't_char': t_char
}
# print out the file info
file_info_keys = ('file name', 'file size', 'last modified', 'last accessed',
                  'creation time', 'Total number of lines are',
                  'Total number of characters are')
file_info_vales = (file_info['fname'],  str(file_info['fsize']) + " bytes",
                   file_info['f_lm'], file_info['f_la'], file_info['f_ct'],
                   file_info['no_of_lines'], file_info['t_char'])

for f_key, f_value in zip(file_info_keys, file_info_vales):
    print(f_key, ' =', f_value)

# check the `file` is direcotry
# print out the file stats
if stat.S_ISDIR(file_stats[stat.ST_MODE]):
    print("This a directory.")
else:
    file_stats_fmt = ''
    print("\nThis is not a directory.")
    stats_keys = ("st_mode (protection bits)", "st_ino (inode number)",
                  "st_dev (device)", "st_nlink (number of hard links)",
                  "st_uid (user ID of owner)", "st_gid (group ID of owner)",
                  "st_size (file size bytes)",
                  "st_atime (last access time seconds since epoch)",
                  "st_mtime (last modification time)",
                  "st_ctime (time of creation Windows)")
    for s_key, s_value in zip(stats_keys, file_stats):
        print(s_key, ' =', s_value)

# 鸡兔同笼问题
class num():
    def __init__(self, a,b):
        self.a = a
        self.b = b

    def num_anamial(a,b):
        num_head=a
        num_feet=b

        num_t1 = (num_feet - num_head * 2) / 2
        num_t2 = (num_feet - num_head * 2)
        if (num_t2%2==0):
            num_j=num_head-num_t1
            print("兔子的数量是：",num_t1,"鸡的数量是：",num_j)
        else :
            print("题目错误，无法计算")

    def num_check(a,b):
        num_head=a
        num_feet=b
        result=0
        if not isinstance(a,int) or not isinstance(b,int) :
            print("输入错误,请输入数字")
            result = 1
            exit(1)
        elif (a<=0 or b<=0):
            print("输入错误，请输入整数")
            result=1
            exit(1)
        elif (num_head>num_feet/2 or num_head<num_feet/4):
            print("输入数据错误，无法计算！！！")
            result = 1
            exit(1)
        else :
            result = 0
            print("参数校验通过...")
        return  result

    def main(a,b):
        num.num_check(a,b)
        num.num_anamial(a,b)

# if __name__ == '__main__':
#     x1=num
#     x1.main(20,44)


# def read_excel():
#     df=pd.read_excel('D:/work2/test_python.xlsx',sheet_name='resv')
#     print(df.loc[[2,5],['id','name','age']].values)
#     cc=df.columns.values
#     ind=df.index.values
#     print(cc)
#     for ix in ind:
#         for ic in cc:
#             print(df.loc[ix,[ic]].values)
# read_excel()



def diff_hotel(new_hotels,old_hotels):
    new_hotels=new_hotels.split(" ")
    old_hotels=old_hotels.split(" ")
    add_hotel=[]
    for new_hotel in new_hotels:
        if new_hotel not in old_hotels:
            add_hotel.append(new_hotel)
    return add_hotel

def check_hotel_add(add_hotel):
    if len(add_hotel) == 0 :
        print("没有新增的酒店")
    else :
        print("有新的酒店")


new_hotel="SLMU SHHZ"
old_hotel="SLMU"
add_hotel=diff_hotel(new_hotel,old_hotel)
print(add_hotel)
check_hotel_add(new_hotel)
check_hotel_add(add_hotel)


class Person():
    def wark(self):
        print("Person is walking...")


class Man(Person):
    def talk(self):
        print("Man is talking...")
    # def wark(self):
    #     print("Man is warking...")

a=Man()
a.wark()
a.talk()

def leap_year(year_num):
    if year_num % 4 == 0 and year_num % 400 == 0 and year_num % 100 != 0 :
        print('{0}是闰年'.format(year_num))
    else :
        print('{0}不是闰年'.format(year_num))

leap_year(2100)


#质数算法

def zhishu(num):
    for n in range(2,num):
        if num % n == 0 :
            print('{0}不是质数'.format(num))
            break
        else :
            print('{0}是质数'.format(num))
            break
zhishu(13)





# import numpy as np
# import math
# import matplotlib.pyplot as plt
# x=np.arange(0.01,3,0.0001)
# y1=[math.log(a,1.5)for a in x]
# y2=[math.log(a,2)for a in x]
# y3=[math.log(a,3)for a in x]
# plot1=plt.plot(x,y1,'-g',label="log1.5(x)")
# plot2=plt.plot(x,y2,'-r',label="log2(x)")
# plot3=plt.plot(x,y3,'-b',label="log3(x)")
# plt.legend(loc='hight right')
# plt.show()



list1=list(range(1,11))
list2=[]
index=1
while len(list1) > 3 :

    for i in list1:  #
        if index== 3 :
            a=list1.remove(i)
            list2.append(i)
            index=2
        else :
            index += 1
print(list2)


def yueSeFu(m,n,k):
    serial_num = list(range(1,m +1))    # 创建从1到m的序号
    index = 0                            # 设置外部变量index
    while len(serial_num) > m - n:        # 当最后剩余人数为m - n之前，一直进行下面的程序
        for i in serial_num:            # 遍历每个编号
            index += 1                     # 把外部变量index进行真实遍历
            if index == k:                # 当外部变量index找到k时，进行下面代码块的操作
                serial_num.remove(i)    # 移除需要下船的人的编号
                index = 1                # 这时候index已经找到序号k了，就要重新遍历
                print('{0}号人下船了'.format(i))

# if __name__ == '__main__':
#     # 传入起始人数m，需要下船的人数n，数到多少下船的序号k,这里可自行设置
#     yueSeFu(10,7,3)

#冒泡

list_sort=[2,4,3,9,12,6,7,11,1,5,10]


def maopao(arr):
    for i in range(len(arr)):
        for j in range(0,len(arr)-1):
            if arr[j] > arr[j+1]:
                arr[j],arr[j+1] = arr[j+1],arr[j]
    print(arr)


#maopao(list_sort)

#选择
def select_sort(arr):
    for i in range(len(arr)-1):
        index=i  #最大值
        for j in range(i+1,len(arr)):
            if arr[index]< arr[j]:
                index=j
        arr[i],arr[index]=arr[index],arr[i]

    print(arr)


#select_sort(list_sort)

#插入排序

def charu_sort(arr):
    for i in range(len(arr)):
        index=i-1
        change_num=arr[i]
        while index >= 0 and change_num < arr[index]:
           arr[index] ,arr[index+1] = change_num,arr[index]
           index-=1
    print(arr)

charu_sort(list_sort)

#优惠券
import random
import string

forSelect = string.ascii_letters + string.digits


def generate_code(count, length):
    for x in range(count):
        Re = ""
        for y in range(length):
            Re += random.choice(forSelect)
        print(Re)
generate_code(10,20)



# coding=utf-8
import os
import re
def deal_text(dir_file,top_n):
    world_match=re.compile(r'\w+')
    with open(dir_file,'r') as f:
        #print(f.read())
        worlds=world_match.findall(f.read().lower())
        dict_test={}
        for world in worlds:
            if world in ['a', 'the', 'to','i']:
                continue
            dict_test[world]=dict_test.get(world,0)+1
    #print(dict_test)
    item = list(dict_test.items())
    item.sort(key=lambda x:(x[1],x[0]),reverse=True)
    if top_n>len(item):
        top_n=len(item)
    for i in range(top_n):

        word, count = item[i]
        print("{0:<10}{1:>5}".format(word, count))

def input_path(dir,top_n):
    if not os.path.isdir(dir):
        print("It's not a dir ~ ")
        return 1
    file_list=os.listdir(dir)
    print(file_list)
    re_match = re.compile(r'\.txt$')
    for file in file_list:
        if re_match.findall(file):
            print("{0} 是日志文件,字符统计如下:".format(file))
            deal_text(dir+file,top_n)
        else:
            print("{0} 不是日志文件".format(file))
input_path('D:/test/test1/',8)

#deal_text('D:/test/test1/20200601.txt')