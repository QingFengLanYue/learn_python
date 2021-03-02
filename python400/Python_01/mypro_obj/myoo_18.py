#测试单例模式

class MySingleton:

    __obj = None           #类属性
    __init_flag = True

    def __new__(cls, *args, **kwargs):
        if cls.__obj ==None:
            cls.__obj = object.__new__(cls)

        return cls.__obj

    def __init__(self,name):
        if MySingleton.__init_flag:
            print("init.....")
            self.name = name
            MySingleton.__init_flag = False

a = MySingleton("aa")
b = MySingleton("bb")
print(a)
print(b)
c = MySingleton("cc")
print(c)
