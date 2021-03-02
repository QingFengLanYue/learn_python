import random
import pymysql
from test01.mm import  __main__

def conn_mysql(name):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='test', charset='utf8')
    cur = conn.cursor()
    cur.execute('select * from test.test1 where name_id=%s'%(name))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def check_name(name):
    a=conn_mysql(name)
    if len(a)==0:
        user_passwd=''
        user_key=''
        result_name = 0
        print("{0}用户名不存在".format(name))
    else:
        st = conn_mysql(name)[0]

        user_key = st[1]
        user_passwd = st[2]
        result_name = 1

    return name,user_key,user_passwd,result_name
#check_name(13)

# #检测密码是否正确
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
    key, res = jiami(passwd)
    # key='edrcq'
    # res='lhcnbsz'
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='test', charset='utf8')
    cur = conn.cursor()
    cur.execute('insert into test1 values(%s,"%s","%s");' % (name,key,res))
    cur.execute('COMMIT;')
    cur.close()
    conn.close()
#write_name("lisi","1234")
def jiami(key_words):
    num=random.randint(3,8)
    key=''.join(random.sample('abcdefghijklmnopqrstuvwxyz',num))
    type='A'

    res=__main__(key,key_words,type)
    return key,res

# write_name(66,'helllow')
# key,res=jiami('helllow')
# print(key,res)

def jiemi(key,res):
    type='j'

    res=__main__(key,res,type)
    return res

#主函数
def name_input(name,passwd):
    passwd=str(passwd)
    user_name,user_key,user_passwd, result_name = check_name(name)


    if result_name == 1 :
        user_passwd1 = jiemi(user_key, user_passwd)  # 解密后的密码
        check_log = login_check(name, passwd, user_name, user_passwd1)
        if check_log == 0 :
            num=1
            while num < 3 :
                passwd=str(input("请重新输入密码:"))
                #passwd=22
                check_log = login_check(name, passwd, user_name, user_passwd1)
                if check_log == 1 :
                    num = 3
                else :
                    num += 1
                    print("密码已经输错{0}次,总共3次机会".format(num))
    else :
        write_log=input("是否进行账户的注册(Y/N):")
        if write_log.upper() == "Y" :
            print("注册的用户名为:{0}".format(name))
            passwd = input("请输入密码:")
            write_name(name, passwd)
            print("恭喜{0}用户注册成功!".format(name))

if __name__ == '__main__':

    name = input('请输入用户名: ')
    passwd = input('请输入密码: ')
    name_input(name,passwd)


# user_name,user_key,user_passwd, result_name = check_name(name)
# user_passwd1 = jiemi(user_key, user_passwd)
# print(user_name,user_key,user_passwd, result_name,user_passwd1)
# user_passwd1 = jiemi('hnayg', 'xjepwdrr')
# print(user_passwd1)
# user_passwd1=jiemi(user_key,user_passwd)
# #write_name(13,14)
# user_name,user_key,user_passwd, result_name = check_name(name)
# check_log = login_check(name, 22, 13, 22)