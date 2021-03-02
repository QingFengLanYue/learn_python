# from multiprocessing import Process,Queue  #导入Process和Queue
# import os,time,random
#
# def write(q):  #定义函数,接收Queue的实例参数
#     for v in range(10):
#         print('Put %s to Queue'%v)
#         q.put(v)  #添加数据到Queue
#         time.sleep(1)
# def read(q): #定义函数，接收Queue的实例参数
#     while True:
#         if not q.empty(): #判断，如果Queue不为空则进行数据取出。
#             v = q.get(True) #取出Queue中的数据，并返回保存。
#             print('Get %s from Queue'%v)
#             time.sleep(1)
#         else: #如果Queue内没有数据则退出。
#             break
#
# if __name__ == '__main__':
#     q = Queue() #实例化Queue括号内可选填，输入数字表示有多少个存储单位。以堵塞方式运行。必须等里边有空余位置时，才能放入数据，或者只能等里边有数据时才能取出数据，取不出数据，或者存不进数据的时候则会一直在等待状态。
#     pw = Process(target=write,args=(q,)) #实例化子进程pw,用来执行write函数，注意这里的函数不带括号，只是传递引用，参数需要使用args参数以元组的方式进行接收。
#     pr = Process(target=read,args=(q,)) #实例化子进程pr,用来执行read函数，注意这里的函数不带括号，只是传递引用，参数需要使用args参数以元组的方式进行接收。
#     pw.start() #开始执行pw。
#     pr.start() #开始执行pr。
#     pw.join() #等待pw结束
#     pr.join() #等待pr结束
#     print('Over')  #主进程结束





# from threading import Thread,Lock #导入互斥锁Lock
#
# num = 0
#
# def work():
#     global num
#     l.acquire() #这里表示调用互斥锁上锁方法，如果work函数先运行l.acquire的话，那么后边的程序就不能再修改和使用变量num。直到将其解锁后才能使用。
#     for i in range(1000000):
#         num += 1
#     print('work的num是%d'%num)
#     l.release() #这里表示调用互斥锁解锁方法。
#
# def works():
#     global num
#     l.acquire() #这里表示调用互斥锁上锁方法。
#     for i in range(1000000):
#         num += 1
#     print('works的num是%d'%num)
#     l.release() #这里表示调用互斥锁解锁方法。
#
#
# l = Lock() #实例化互斥锁，互斥锁是为了保护子线程不争抢数据而使用的一个类。
# t = Thread(target=work)
# tt = Thread(target=works)
# t.start()
# tt.start()
# print('最后的num值是%d'%num) #输出最后的结果，如果实验过的可能会发现这个结果并不是2000000，为什么呢？




# import threading
# import time
#
# class MyThread(threading.Thread):
#     def run(self):
#         global num
#         time.sleep(1)
#
#         if mutex.acquire(1):
#             num = num+1
#             msg = self.name+' set num to '+str(num)
#             print (msg)
#             mutex.release()
# num = 0
# mutex = threading.Lock()
# def test():
#     for i in range(5):
#         t = MyThread()
#         t.start()
# if __name__ == '__main__':
#     test()


class Employee:
    '所有员工的基类'
    empCount = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def displayCount():
        print("Total Employee %d" % Employee.empCount)

    def displayEmployee(self):
        print("Name : ", self.name, ", Salary: ", self.salary)





"创建 Employee 类的第一个对象"
emp1 = Employee("Zara", 2000)
"创建 Employee 类的第二个对象"
emp2 = Employee("Manni", 5000)
emp1.displayEmployee()
emp2.displayEmployee()
print(Employee.displayCount())

import threading
import time
import queue

q = queue.Queue(maxsize=8)   #q在t1和t2两个子线程之间通信共享，一个存入数据，一个使用数据。
def t1(q):
    for i in range(10):
        q.put(i)
def t2(q):
    while not q.empty():
        print('队列中的数据量：'+str(q.qsize()))
        # q.qsize()是获取队列中剩余的数量
        print('取出值:'+str(q.get()))
        # q.get()是一个堵塞的，会等待直到获取到数据
        print('-----')
        time.sleep(0.01)
t1 = threading.Thread(target=t1,args=(q,))
t2 = threading.Thread(target=t2,args=(q,))
t1.start()
t2.start()


def run1():
    while 1:
        if l1.acquire():
            # 如果第一把锁上锁了
            print('我是老大，我先运行')
            l2.release()
            # 释放第二把锁
def run2():
    while 1:
        if l2.acquire():
            # 如果第二把锁上锁了
            print('我是老二，我第二运行')
            l3.release()
            # 释放第三把锁
def run3():
    while 1:
        if l3.acquire():
            # 如果第三把锁上锁了
            print('我是老三，我最后运行')
            l1.release()
            # 释放第一把锁
t1 = threading.Thread(target=run1)
t2 = threading.Thread(target=run2)
t3 = threading.Thread(target=run3)

l1 = threading.Lock()
l2 = threading.Lock()
l3 = threading.Lock()
# 实例化三把锁

l2.acquire()
l3.acquire()

# t1.start()
# t2.start()
# t3.start()


import threading
import time
import random

boys = ['此时一位捡瓶子的靓仔路过\n------------','此时一位没钱的网友路过\n------------','此时一位推着屎球的屎壳郎路过\n------------']
event = threading.Event()
def lighter():
    event.set()
    while 1:
        ti = (random.randint(1, 10))
        time.sleep(ti)
        print('等待 {} 秒后'.format(str(ti)))
        event.clear()
        time.sleep(ti)
        event.set()


def go(boy):
    while 1:
        if event.is_set():
            # 如果事件被设置
            print('在辽阔的街头')
            print(boy)
            time.sleep(random.randint(1, 5))
        else:
            print('在寂静的田野')
            print(boy)
            event.wait()
            print('突然，一辆火车驶过')
            time.sleep(5)

t1 = threading.Thread(target=lighter)
t1.start()

for boy in boys:
    t2 = threading.Thread(target=go,args=(boy,))
    t2.start()
