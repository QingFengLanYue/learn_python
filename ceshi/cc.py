import sys
import random
import pandas as pd
import os

def red_qiu():
    list = []
    while len(list) != 6:
        red=random.randint(1,32)
        if red not in list:
            list.append(red)
    return list

def blue_qiu():
    blue=random.randint(1,16)
    return blue
def win(df2,win_num):
    #01 04 12 20 25 32 02
    '''
     中0-2个红球1个蓝球是六等奖—5元。中3个红球1个蓝球或4个红球是五等奖—10元。

    中4个红球一个蓝球或五个红球是四等奖—200元。中5个红球一个蓝球是三等奖—3000元。

    只中6个红球是二等奖—最高500万元。全部猜中为一等奖—最高1000万元。

    '''
    first1, two1, three1, four1, five1, six1 =  0, 0, 0, 0, 0, 0
    #df2 = pd.read_csv(file)
    for indexs in df2.index:
        red=0
        blue=0
        for red_num in df2.loc[indexs].values[0:6]:
            #print(red_num)
            if red_num in win_num[0:6]:
                red+=1

        for blue_num in df2.loc[indexs].values[6:7]:
            if blue_num == win_num[6]:
                blue=1
        first,two,three,four,five,six=jiangxiang(red,blue)
        if first == 1 :
            print('恭喜第:%s名用户斩获一等奖:%s'%(indexs,df2.loc[indexs].values))
            first1+=1
        elif two == 1 :
            print('恭喜第:%s名用户斩获二等奖:%s'%(indexs,df2.loc[indexs].values))
            two1+=1
        elif three == 1 :
            print('恭喜第:%s名用户斩获三等奖:%s'%(indexs,df2.loc[indexs].values))
            three1+=1
        elif four == 1 :
            four1+=1
        elif five == 1 :
            five1+=1
        elif six == 1 :
            six1+=1
    return first1, two1, three1, four1, five1, six1



def jiangxiang(red,blue):
    first, two, three, four, five, six=0,0,0,0,0,0
    if red <= 2 and blue == 1 :
        six=1
    elif (red == 3 and blue == 1) or (red == 4 and blue ==0 ):
        five=1
    elif (red == 4 and blue == 1) or (red == 5 and blue ==0 ):
        four=1
    elif (red == 5 and blue == 1) :
        three=1
    elif (red == 6 and blue == 0) :
        two=1
    elif (red == 6 and blue == 1) :
        first=1

    return first,two,three,four,five,six

def win_num_random():
    red = sorted(red_qiu())
    blue = blue_qiu()
    red.append(blue)
    return red


def anay_cc(g_num,win_num,file):
    li = []
    for i in range(g_num):
        red=sorted(red_qiu())
        blue=blue_qiu()
        red.append(blue)

        li.append(red)

    order = ['1', '2','3','4','5','6','7']
    df = pd.DataFrame(li,columns=order)
    print('开始写入文件。。。')
    #df.to_csv(file,index=False)
    print('开始分析文件。。。')
    print('-----------------------------------------------------------')
    first1,two1,three1,four1,five1,six1=win(df,win_num)
    totol_win=six1*5+five1*10+four1*200+three1*3000+two1*291499+first1*5000000
    totol_money=g_num*2
    hbl=totol_win/totol_money*100
    print('-----------------------------------------------------------')
    print('一等奖:%s\n二等奖:%s\n三等奖:%s\n四等奖:%s\n五等奖:%s\n六等奖:%s'
          % (first1, two1, three1, four1, five1, six1 ))
    print('总花费为：%s元' %(totol_money))
    print('总奖金为：%s元'%(totol_win))
    print('回报率为:%.2f%%'%hbl)
    return hbl
    # win_num = [1, 4, 12, 20, 25, 32, 2]
    # order = ['1', '2', '3', '4', '5', '6', '7']
    # df = pd.DataFrame([[1,4,12,20,25,32,4],[1,4,12,20,25,32,2]], columns=order)
    # win(df,win_num=[1,4,12,20,25,32,2])

def cs():
    #win_num=[5,6,14,16,19,27,10]
    win_num=win_num_random()
    print('此次随机的奖号码为：%s'%win_num)
    g_num=10000
    file='D:/work2/cc.csv'

    hbl=anay_cc(g_num,win_num,file)
    return hbl

def con_deal(file):
    if os.path.exists(file):
        with open(file, mode='r+', encoding='utf-8') as f1:
            lines = f1.readlines()
            last_line = lines[-1]  # 取最后一行
            l=last_line.strip('[|]|').strip(' ')
            l1=[]
            for i in l.split(', '):
                l1.append(float(i))
            l2=len(l1)
    else:
        l1 = []
        l2 = 0
    return l1,l2

if __name__=='__main__':

    file='D:/work2/cc.log'
    sys.stdout = open(file, mode='a+', encoding='utf-8')
    rest,i = con_deal(file)
    while True:
        print('开始%s次测试'%i)
        print('#######################################################')
        hbl=cs()
        rest.append(round(hbl,2))
        print(rest)
        i+=1
        sys.stdout.flush()