import datetime
import random
import pymysql
from test01.mm import main as mm
from test01.passwd_check import passwd_check

# CREATE TABLE test.user(
# id bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
# user_name varchar(20)  NOT NULL COMMENT '用户名',
# keyword varchar(10)  NOT NULL COMMENT '关键字',
# passwd varchar(50)  NOT NULL COMMENT '密码',
# PRIMARY KEY (`id`)
# )

# CREATE TABLE test.user_log (
#   `id` bigint(10) unsigned NOT NULL AUTO_INCREMENT,
#   `user_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
#   `login_num` tinyint(4) NOT NULL DEFAULT '1' COMMENT '登录次数',
#   `login_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#   `login_result` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0:faile ,1 sucess',
#   PRIMARY KEY (`id`)
# )

#装饰器，捕捉sql异常
def decorate(func):
    def except_deal(sql):
        try:
            return func(sql)
        except pymysql.err.ProgrammingError as e:
            print('Sql 语句报错', e)
            # 捕获由于sql语句错误抛出的异常
            # 捕获后的操作
        except pymysql.err.IntegrityError as e:
            print('主键冲突,请核对后重新输入\n', e)

    return except_deal

#mysql 连接
def con_my():
    host='localhost'
    port=3306
    user='root'
    password='root'
    db='test'
    conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8')
    cur = conn.cursor()
    return conn,cur

def select_sql(name):
    sql="select user_name,keyword,passwd from test.user where user_name='%s';"%(name)
    return sql


@decorate
def check_exists(sql):
    conn,cur = con_my()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def check_name(name):
    s_sql=select_sql(name)
    check_res=check_exists(s_sql)
    if len(check_res)==0:
        user_passwd=''
        user_key=''
        result_name = 0
        print("{0}用户名不存在".format(name))
    else:
        st = check_res[0]

        user_key = st[1]
        user_passwd = st[2]
        result_name = 1

    return name,user_key,user_passwd,result_name
#check_name(13)

# #检测密码是否正确
def login_check(name,passwd,user_name,user_passwd):
    if name == user_name and passwd == user_passwd:
        check_log = 1
    else :
        check_log = 0
    return check_log

#login_check("zhangsan","123","zhangsan","1234")

def insert_sql(name,passwd):
    key, res = jiami(passwd)
    sql='insert into test.user(user_name,keyword,passwd) values("%s","%s","%s");' % (name,key,res)
    return sql

#注册用户
@decorate
def write_name(sql):
    #key, res = jiami(passwd)
    # key='edrcq'
    # res='lhcnbsz'
    conn, cur = con_my()
    cur.execute(sql)
    cur.execute('COMMIT;')
    cur.close()
    conn.close()
#write_name("lisi","1234")

def jiami(key_words):
    num=random.randint(3,8)
    key_pol=[chr(a) for a in range(33,127)]
    key=''.join(random.sample(key_pol,num))
    type='A'

    res=mm(key,key_words,type)
    return key,res

# write_name(66,'helllow')
# key,res=jiami('helllow')
# print(key,res)

def jiemi(key,res):
    type='j'

    res=mm(key,res,type)
    return res

#检查输入是否正确，最多输错三次
def check_num(name, passwd, user_name, user_passwd1):
    num = 0
    reslut = 0
    while num < 3:
        check_log = login_check(name, passwd, user_name, user_passwd1)
        # passwd=22
        if check_log == 1:
            print("{0}用户登录成功~".format(name))
            num += 1
            reslut = 1
            break
        else:
            num += 1
            print("{0}密码输入错误,登陆失败~".format(name))
            print("密码已经输错{0}次,总共3次机会!".format(num))
            if num != 3:
                passwd = str(input(r"请重新输入密码: "))
    return num ,reslut


def passwd_check_num(passwd):
    n = 0
    result = 0
    while n < 5:
        passwd_check_res=passwd_check(passwd)
        if passwd_check_res == 1:
            #print("{0}用户登录成功~".format(name))
            n = 5
            result = 1
            passwd = passwd
        else:
            n += 1
            if n != 5:
                passwd = str(input(r"请重新输入密码: "))
    return result,passwd



def get_now_time():
    now_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now_time



def insert_log(name,now_time,login_num,login_result):
    sql = 'insert into test.user_log(user_name,login_time,login_num,login_result)  values("%s","%s","%s","%s");' \
          % (name,now_time,login_num,login_result)
    return sql

#主函数
def name_input(name,passwd):
    passwd=str(passwd)
    user_name,user_key,user_passwd, result_name = check_name(name)


    if result_name == 1 :
        user_passwd1 = jiemi(user_key, user_passwd)  # 解密后的密码
        login_num,login_result = check_num(name, passwd, user_name, user_passwd1)
        now_time = get_now_time()
        log_sql = insert_log(name,now_time,login_num,login_result)
        write_name(log_sql)
    else :
        write_log=input("是否进行账户的注册(Y/N): ")
        if write_log.upper() == "Y" :
            print("注册的用户名为:{0}".format(name))
            passwd = input(r"请输入密码: ")
            pass_check_res,passwd = passwd_check_num(passwd)
            #print(pass_check_res,passwd,type(pass_check_res),type(passwd))
            if pass_check_res == 1:
                i_sql = insert_sql(name,passwd)
                #print(i_sql)
                write_name(i_sql)

                print("恭喜{0}用户注册成功!".format(name))
            else :
                print("{0}用户注册失败!".format(name))

if __name__ == '__main__':

    name = input(r'请输入用户名: ')
    passwd = input(r'请输入密码: ')
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