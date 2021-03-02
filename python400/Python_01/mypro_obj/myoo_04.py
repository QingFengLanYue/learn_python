#测试类方法
class Student:
    company = "尚学堂"  # 类属性

    @classmethod
    def printCompany(cls):
        print(id(cls))
        print(cls.company)


Student.printCompany()

print(id(Student))

