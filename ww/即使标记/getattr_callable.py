"""
author:cai
project:learn_python
date:2021/7/29
"""
# coding=utf8

class A:
    def __init__(self):
        self.name = 'zhangjing'

# 　　  # self.age='24'
    def method(self,lz):
        print(lz)


Instance = A()
print(getattr(Instance, 'name', 'not find')) #如果Instance 对象中有属性name则打印self.name的值，否则打印'

print(getattr(Instance, 'age', 'not find'))  # 如果Instance 对象中有属性age则打印self.age的值，否则打印'not find'
print(getattr(A, 'method', 'default'))
# 如果有方法method，否则打印其地址，否则打印default
print(getattr(Instance, 'method', 'default'))

# 如果有方法method，运行函数并打印None否则打印default

print(callable(A.method))