# 简易加密解密
#维热纳尔方阵加密
import math


def start(key, key_words):
    bs = math.ceil(len(key_words) / len(key))
    key1 = key * bs
    key2 = key1[0:len(key_words)]
    return key2, key_words


def start2():
    list1 = []
    for i in range(97, 123):
        list1.append(chr(i))
    # print (list1)

    list3 = []
    for i in range(26):
        list2 = list1[i:] + list1[0:i]
        list3.append(list2)
    return list3


def add_p(key, key_words, list3, type ):
    list4 = []
    for num in range(len(key_words)):
        for i in range(26):
            a = list3[i][0]
            if (a == key[num]):
                # print('选取的密码行为',i)
                if (key_words[num] == ' '):
                    list4.append(' ')
                for j in range(26):
                    if (type=='j'):

                        if (list3[i][j] == key_words[num]):
                            # print('加密取的位置',j)
                            # print('加密的结果为：',list3[0][j])
                            # print(list3[i][j])

                            list4.append(list3[0][j])
                    elif (type=='a'):
                        if (list3[0][j] == key_words[num]):
                            # print('加密取的位置',j)
                            # print('加密的结果为：',list3[i][j])
                            # print(list3[i][j])

                            list4.append(list3[i][j])

        num = num + 1
    if(type=='a'):
        print('总共加密 %s 次' % num)
    elif(type=='j'):
        print('总共解密 %s 次' % num)

    res = ("".join(list4))
    return res

def __main__(key,key_words,type):
    key=key.lower()
    key_words=key_words.lower()
    type=type.lower()
    key1, key_words = start(key, key_words)
    list3 = start2()
    res = add_p(key1, key_words, list3, type)
    #print("key:%s,key_words:%s,type:%s,结果 %s" % (key, key_words, type, res))
    return res


