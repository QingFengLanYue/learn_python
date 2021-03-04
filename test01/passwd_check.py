# def cc():
#     a=input('1:')
#     b=input('2:')
#     if a == b:
#         c=1
#     else :
#         c=0
#     return c
# def ss():
#     n=0
#     while n < 3:
#         c=cc()
#         if c==1:
#             print('OK')
#             n=3
#         else :
#             n += 1
#             print('已经错了%s'%n)
# ss()


def passwd_judge1(advice: list,passwd: str):
    grade1 = 0
    if len(passwd) < 8:
        advice.append("你的密码长度小于8，请重试!")
    else:
        grade1 = 1
    return grade1


# 数字，字母，特殊字符的判断




def passwd_judge2(advice,passwd: str):
    result = [0, 0, 0, 0]
    grade2 = 0
    for i in passwd:

        if i.isupper():
            result[0] = 1
        elif i.islower():
            result[1] = 1
        elif i.isdigit():
            result[2] = 1
        else:
            result[3] = 1
    if sum(result) < 3 :

        advice.append("你的密码需要包括大、小写字母.数字.其它符号,以上四种至少三种!")
    else:
        grade2 = 1
    return grade2


# 重复子串判断

def passwd_judge3(advice,passwd: str):
    global grade1
    grade1 = 0
    for a in range(len(passwd)-3):
        if passwd.count(passwd[a:a + 3]) > 2:
            advice.append("你的密码有长度超过或等于3的子串连续重复！")
            break
        else:
            grade1 = 1
    return grade1


def passwd_check(passwd :str):
    grade = 2
    advice = []
    grade1 = passwd_judge1(advice,passwd)
    grade3 = passwd_judge3(advice,passwd)
    grade2 = passwd_judge2(advice,passwd)
    if grade1 == 1:
        grade += 1

    if grade2 == 1:
        grade += 1

    if grade3 == 1:
        grade += 1

    if grade >= 5:
        print('密码复杂度为:%s,校验结果:通过~' % (grade))
        check = 1
    else:
        print('密码复杂度为:%s,校验结果:%s' % (grade,advice))
        check = 0
    return check
