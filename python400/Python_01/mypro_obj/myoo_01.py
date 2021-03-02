class Student:   #类名一般首字母大写，多个单词采用驼峰原则

    def __init__(self,name,score): #self必须位于第一个参数
        self.name = name
        self.score = score

    def say_score(self):   #self必须位于第一个参数
        print("{0}的分数是：{1}".format(self.name,self.score))



s1 = Student("高淇",18)   #通过类名()调用构造函数
s1.say_score()

s1.age = 32
s1.salary = 3000
#del s1
print(s1.salary)

s2 = Student("高希希",100)
s2.say_score()
Student.say_score(s2)

print(dir(s2))

print(s2.__dict__)

class Man:
    pass


print(isinstance(s2,Man))

