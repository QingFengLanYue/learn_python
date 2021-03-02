# encoding=utf-8
import os
import pymysql
def login():
    # name = input("请输入用户名：")
    # passwd = input("请输入密码：")
    name="lisi"
    passwd="123"
    with open ('D:/test/test1/user.txt','r') as user:
        result_log = 0
        infos = user.readlines()
        for info in infos:
            user_name,user_passwd = info.split(":")
            if name == user_name and passwd == user_passwd:
                print("登陆成功~")
                result_log = 1

        if result_log == 0:
            print("登陆失败~,用户名不存在")
        if result_log == 2:
            print("输入密码错误,已输入错误{0}次,请重新输入!")

#login()

#检察用户名是否存在,获取密码
def check_name(name):
    file='D:/test/test1/user.txt'
    with open(file, 'r') as user:
        result_name = 0
        infos = user.readlines()
        for info in infos:
            user_name = info.split(":")[0]
            if name == user_name and user_name is not None:
                #print("{0}用户存在~".format(name))
                result_name = 1
                user_passwd = info.split(":")[1]
        if result_name == 0 :
            user_passwd=''
            print("{0}用户名不存在".format(name))
    return name,user_passwd,result_name
#check_name("lisi")

#检测密码是否正确
def login_check(name,passwd,user_name,user_passwd):

    check_log = 0
    if name == user_name and passwd == user_passwd:
        print("{0}用户登录成功~".format(name))
        check_log = 1
    if check_log == 0:
        print("{0}密码输入错误,登陆失败~".format(name))
    return check_log

#login_check("zhangsan","123","zhangsan","1234")

#注册用户
def write_name(name,passwd):
    file='D:/test/test1/user.txt'
    with open(file, 'a+') as user:
        s = os.path.getsize(file)
        if s == 0:
            str = name + ':' + passwd
        else:
            str = '\n' + name + ':' + passwd
        user.write(str)

#write_name("lisi","1234")
#主函数
def name_input(name,passwd):

    user_name,user_passwd, result_name = check_name(name)
    if result_name == 1 :
        check_log = login_check(name, passwd, user_name, user_passwd)
        if check_log == 0 :
            num=1
            while num < 3 :
                passwd=input("请重新输入密码:")
                check_log = login_check(name, passwd, user_name, user_passwd)
                if check_log == 1 :
                    num = 3
                else :
                    num += 1
                    print("密码已经输错{0}次,总共3次机会".format(num))
    else :
        write_log=input("是否进行账户的注册(Y/N):")
        if write_log == "Y" :
            print("注册的用户名为:{0}".format(name))
            passwd = input("请输入密码:")
            write_name(name, passwd)
            print("恭喜{0}用户注册成功!".format(name))


name = "zhaoliu4"
passwd = "12"
name_input(name,passwd)
#check_name(name)