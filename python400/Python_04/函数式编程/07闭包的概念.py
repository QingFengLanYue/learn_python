'''
1.什么是闭包
   闭包其实就是一个函数
2.如何创建闭包
  a.要有函数的嵌套(外部函数、内部函数)
  b.内部函数中要使用外部函数的变量
  c.外部函数必须有返回值，返回内部函数名
3.如何使用闭包
    f=funOut(100)   #调用外部函数，用f变量指向内部函数
    print(type(f))
    result=f(200)    #通过变量调用函数
'''

#使用闭包，完成求两个数的和
def sum(a,b):
    return a+b

def funOut(num1):
    def funIn(num2):
        #内部函数修改外部函数的变量
        nonlocal num1
        num1+=100
        return num2+num1
    return funIn

funIn=funOut(100)
print(type(funIn))
result=funIn(200)
print('两个数的和：',result)