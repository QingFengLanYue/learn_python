#测试@property的最简化的使用

class Employee:

    @property
    def salary(self):
        print("salary run...")
        return 10000


emp1 = Employee()
#emp1.salary()
print(emp1.salary)
