#嵌套函数

b = 300

def f1():
    print("f1 running")
    a = 200

    def f2():
        global b            #声明全局变量
        nonlocal a          #声明外层的局部变量
        print("f2 running,",a)
        a = 100
        b = 1000

    f2()                        #f2是嵌套函数，只能在f1中被调用。

    print(a)

f1()
print(b)