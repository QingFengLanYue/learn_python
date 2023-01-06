# 利率的计算

# 等额本金

'''
等额bai本息的计算公式为：每月还本付息金额=[贷款本金×月利率×(1+月利率)^还款月数]÷[(1+月利率)^还款月数-1]，其中“^”表示“乘方”。
等额本金的计算公式为：每月还本付息金额=（本金/还款月数）+（本金－累计已还本金）×月利率

'''


class lvv:

    def __init__(self, year, lv, amount):
        self.year = year
        self.lv = lv
        self.amount = amount

    def dengEBenXi(self):
        amountMon = self.year * 12
        lv1 = self.lv / 100 / 12
        monAmount = (self.amount * lv1 * (1 + lv1) ** amountMon) / ((1 + lv1) ** amountMon - 1)
        totalAmount = monAmount * amountMon
        print('等额本息总共还贷款金额为：%.2f,平均每月还款：%.2f' % (totalAmount, monAmount))

    def dengEBenJin(self):
        amountMon = self.year * 12
        lv1 = self.lv / 100 / 12
        totalAmount = 0
        list1 = []
        diJianAmount = (self.amount / amountMon) * lv1
        for i in range(1, amountMon + 1):
            monAmount = (self.amount / amountMon) + (self.amount - i * (self.amount / amountMon)) * lv1
            list1.append(monAmount)
            totalAmount = sum(list1)
            # print('第%s月份的还款金额为：%.2f'%(i,monAmount))
        print('等额本金总共还贷款金额为：%.2f,平均每月还款：%.f,首月还款金额为：%.2f,最后一月还款金额为：%.2f,每月递减：%.2f' \
              % (totalAmount, totalAmount / amountMon, list1[0], list1[-1], diJianAmount))

    def mian_lv(self):
        print(f'贷款{self.amount}万,贷款{self.year}年,利率{self.lv},还款内容如下：')
        self.amount = self.amount*10000
        self.dengEBenJin()
        self.dengEBenXi()


if __name__ == '__main__':
    x = lvv(30, 4.8, 97)
    x.mian_lv()
