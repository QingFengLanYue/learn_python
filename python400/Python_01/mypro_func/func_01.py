#测试函数的定义和调用


def  test01():
    print("*"*10)
    print("@"*10)


print(id(test01))
print(type(test01))
print(test01)

test01()
test01()
test01()

for i in range(10):
    test01()
