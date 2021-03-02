#测试可调用方法__call__()

class SalaryAccount:
    '''工资计算类'''

    def __call__(self, salary):
        print("算工资啦...")
        yearSalary = salary*12
        daySalary = salary//22.5  #国家规定的每个月的平均工作天数
        hourSalary = daySalary//8

        return dict(yearSalary=yearSalary,monthSalary=salary,daySalary=daySalary,hourSalary=hourSalary)


s = SalaryAccount()
print(s(30000))