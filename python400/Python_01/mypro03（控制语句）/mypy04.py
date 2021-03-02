#测试选择结构的嵌套
#输入一个分数。分数在0-100之间。90以上是A,80以上是B，70以上是C，60以上是D。60以下是E。

score = int(input("请输入一个在0-100之间的数字："))
grade = ""
if score>100 or score<0:
    score = int(input("输入错误！请重新输入一个在0-100之间的数字："))
else:
    if score>=90:
        grade = "A"
    elif score>=80:
        grade = 'B'
    elif score>=70:
        grade = 'C'
    elif score>=60:
        grade = 'D'
    else:
        grade = 'E'
    print("分数为{0},等级为{1}".format(score,grade))

print("*******************************************************")

score = int(input("请输入一个在0-100之间的数字："))
degree = "ABCDE"
num = 0
if score>100 or score<0:
    score = int(input("输入错误！请重新输入一个在0-100之间的数字："))
else:
    num = score//10
    if num<6:num=5

    print("分数是{0},等级是{1}".format(score,degree[9-num]))