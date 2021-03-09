import math

from urllib3.util import request


class cs:
    def __init__(self,name,passwd):
        self.name = name
        self.passwd = passwd
    def cs1(self):
        print('hahhaha')
    def cs2(self):
        cs.cs1(self)
        print(self.name,self.passwd)

l=cs(name='a',passwd='b')
l.cs2()


class Neuralnetwork(object):
    def __init__(self, data):
        self.data = data

    def scan(self):
        print(self.data)
        pass
    def sigmoid(self, z):
        g = 1 / (1 + math.exp(-z))
        return (g)


# replace data and z with appropriate values
nn = Neuralnetwork(12)
a1 = nn.sigmoid(7)
b1 = nn.scan()
print(a1)



import datetime
from test01.passwd_check import passwd_check
now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(now_time)


def passwd_check_num(passwd):
    n = 0
    result = 0
    while n < 5:
        passwd_check_res=passwd_check(passwd)
        if passwd_check_res == 1:
            #print("{0}用户登录成功~".format(name))
            n = 5
            result = 1
            passwd = passwd
        else:
            n += 1
            if n != 5:
                passwd = str(input(r"请重新输入密码: "))
    return result,passwd


result,passwd=passwd_check_num('aaa')
print(result,passwd)