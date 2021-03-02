#测试函数也是对象

def  test01():
    print("sxtsxt")

test01()
c = test01
c()

print(id(test01))
print(id(c))
print(type(c))

