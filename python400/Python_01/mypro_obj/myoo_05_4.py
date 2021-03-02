#测试私有属性、私有方法

class Employee:

    __company = "百战程序员"

    def __init__(self,name,age):
        self.name = name
        self.__age = age        #私有属性

    def __work(self):           #私有方法
        print("好好工作，赚钱娶媳妇！")
        print("年龄：{0}".format(self.__age))
        print(Employee.__company)



e = Employee("高淇",18)

print(e.name)
#print(e.__age)
print(e._Employee__age)
print(dir(e))
e._Employee__work()
print(Employee._Employee__company)