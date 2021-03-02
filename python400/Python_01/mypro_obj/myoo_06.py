#测试继承的基本使用

class Person:

    def __init__(self,name,age):
        self.name = name
        self.__age = age    #私有属性

    def say_age(self):
        print("年龄，年龄，我也不知道")


class Student(Person):

    def __init__(self,name,age,score):
        Person.__init__(self,name,age)  #必须显式的调用父类初始化方法，不然解释器不会去调用
        self.score = score


#Student-->Person-->object类
print(Student.mro())

s = Student("高淇",18,60)
s.say_age()
print(s.name)
#print(s.age)
print(dir(s))
print(s._Person__age)