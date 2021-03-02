#!/usr/local/bin/python
dict = {'a': 1, 'b': 2, 'b': '3'}
dict['name']='jia'
dict['age']=18
dict[15]=14
print(dict)
#dict.clear()
del dict[15]
print(dict.popitem())

import time
tick=time.time()
localtime=time.localtime(tick)
print(tick,localtime)
print(time.asctime(localtime))
sptime=time.strftime("%Y-%m-%d %H:%M:%S",localtime)
print(sptime)


import calendar

date=calendar.month(2020,2)
print(date)
year=calendar.calendar(2019,w=2,l=0,c=5)
print(year)


def printinfo(arg1, *vartuple):
        "打印任何传入的参数"
        print("输出: ")
        print(arg1)
        for var in vartuple:
                print(var)
        return;


# 调用printinfo 函数
printinfo(10);
printinfo(70, 60, 50);

import os

# 给出当前的目录
# print(os.getcwd())
# os.chdir('C:/Users/HP/Desktop')
# print(os.getcwd())

import re
a = "123abc456"
print(re.search("([0-9]*)([a-z]*)([0-9]*)",a).group(0))   #123abc456,返回整体
print(re.search("([0-9]*)([a-z]*)([0-9]*)",a).group(1))   #123
print(re.search("([0-9]*)([a-z]*)([0-9]*)",a).group(2))   #abc
print(re.search("([0-9]*)([a-z]*)([0-9]*)",a).group(3))   #456



p = re.compile(r'\d{3}-\d{6}')
print(p.findall('0110-211-628888'))


print(re.search(r"(([01]?\d?\d|2[0-4]\d|25[0-5])\.){3}([01]?\d?\d|2[0-4]\d|25[0-5]\.)","192.168.1.1"))


key = r"<html><body><h1>hello world<h1></body></html>"#这段是你要匹配的文本
p1 = r"(?<=<h1>).+?(?=<h1>)"#这是我们写的正则表达式规则，你现在可以不理解啥意思
pattern1 = re.compile(p1)#我们在编译这段正则表达式
matcher1 = re.search(pattern1,key)#在源文本中搜索符合正则表达式的部分
print (p1) #打印出来


key = r"javapythonhtmlvhdl"#这是源文本
p1 = r"python"#这是我们写的正则表达式
pattern1 = re.compile(p1)#同样是编译
matcher1 = re.search(pattern1,key)#同样是查询

print (matcher1.group(0))